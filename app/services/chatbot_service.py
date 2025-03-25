from app.db import MockRPCDatabase
from app.utils.rpc_retrier_wrapper import RPCRetrier
from app.models.models import SurveyResponse, ConversationState
from fastapi import WebSocket, HTTPException
from typing import List, Dict, Any
import logging

# Initialize database and retrier
db = MockRPCDatabase()
retrier = RPCRetrier(max_retries=3, retry_delay=1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Centralized error message
TECHNICAL_DIFFICULTIES_MESSAGE = "We are experiencing technical difficulties. Please try again later."


class ChatbotService:
    """Service layer for chatbot operations."""

    @staticmethod
    async def get_customer_info(customer_id: str) -> Dict[str, Any]:
        """Retrieve customer information."""
        try:
            customer_info = await retrier.call(db.get_customer_info, customer_id)
            if not customer_info:
                raise HTTPException(status_code=404, detail="Customer not found.")
            return customer_info
        except ConnectionError:
            raise HTTPException(status_code=500, detail=TECHNICAL_DIFFICULTIES_MESSAGE)

    @staticmethod
    async def get_survey_questions(survey_id: str) -> List[Dict[str, Any]]:
        """Retrieve survey questions."""
        try:
            survey_questions = await retrier.call(db.get_survey_questions, survey_id)
            if not survey_questions:
                raise HTTPException(status_code=404, detail="Survey not found.")
            return survey_questions
        except ConnectionError:
            raise HTTPException(status_code=500, detail=TECHNICAL_DIFFICULTIES_MESSAGE)

    @staticmethod
    async def get_or_initialize_conversation_state(
        customer_id: str, survey_id: str
    ) -> ConversationState:
        """Retrieve or initialize the conversation state."""
        conversation_id = f"conv_{customer_id}_{survey_id}"
        try:
            state_data = await retrier.call(db.get_conversation_state, conversation_id)
            if state_data:
                state = ConversationState(**state_data)
                return state
            else:
                # Initialize a new conversation state
                state = ConversationState(
                    customer_id=customer_id,
                    current_question=1,
                    completed=False,
                    responses=[],
                    survey_id=survey_id,
                )
                await retrier.call(db.save_conversation_state, conversation_id, state.model_dump())
                return state
        except ConnectionError:
            raise HTTPException(status_code=500, detail=TECHNICAL_DIFFICULTIES_MESSAGE)

    @staticmethod
    async def save_conversation_state(conversation_id: str, state: ConversationState):
        """Save the conversation state."""
        try:
            await retrier.call(db.save_conversation_state, conversation_id, state.model_dump())
        except ConnectionError:
            logger.warning(f"Failed to save conversation state for {conversation_id}.")

    @staticmethod
    async def save_survey_response(response: SurveyResponse):
        """Save a survey response."""
        try:
            await retrier.call(db.save_survey_response, response.model_dump())
        except ConnectionError:
            raise HTTPException(status_code=500, detail=TECHNICAL_DIFFICULTIES_MESSAGE)

    @staticmethod
    async def handle_websocket_interaction(
        websocket: WebSocket, customer_id: str, survey_id: str
    ):
        """Handle the WebSocket interaction for the chatbot."""
        await websocket.accept()

        # Retrieve customer info
        customer_info = await ChatbotService.get_customer_info(customer_id)

        # Retrieve survey questions
        survey_questions = await ChatbotService.get_survey_questions(survey_id)

        # Initialize or retrieve conversation state
        conversation_id = f"conv_{customer_id}_{survey_id}"
        state = await ChatbotService.get_or_initialize_conversation_state(customer_id, survey_id)

        # Check if the survey is already completed
        if state.completed:
            await websocket.send_text(
                f"BOT: You have already completed this survey, {customer_info['name']}. Thank you!"
            )
            await websocket.close()
            return

        try:
            while not state.completed:
                # Send the current question
                try:
                    question = survey_questions[state.current_question - 1]
                    options = question.options
                    options_text = "\n".join([f"{i + 1} - {option}" for i, option in enumerate(options)])
                    await websocket.send_text(
                        f"BOT: {question.question}\nHere are your options:\n{options_text}\n\nPlease reply with the number corresponding to your choice."
                    )
                except IndexError:
                    await websocket.send_text("Invalid question index. Please try again later.")
                    await websocket.close()
                    return

                # Receive the customer's response
                response_data = await websocket.receive_text()

                # Check if the question allows open feedback (e.g., "Yes" selected)
                if "Yes" in options and response_data == "1" and state.current_question == len(survey_questions):
                    await websocket.send_text("BOT: Please provide your feedback in text form.")
                    feedback = await websocket.receive_text()
                    response = SurveyResponse(
                        customer_id=customer_id,
                        question_id=question.id,
                        answer=feedback,
                    )
                else:
                    try:
                        response_index = int(response_data) - 1
                        if response_index < 0 or response_index >= len(options):
                            raise ValueError
                        response = SurveyResponse(
                            customer_id=customer_id,
                            question_id=question.id,
                            answer=options[response_index],
                        )
                    except ValueError:
                        await websocket.send_text(
                            "BOT: Invalid response. Please reply with the number corresponding to your choice."
                        )
                        continue

                # Save the response
                await ChatbotService.save_survey_response(response)
                state.responses.append(response)

                # Move to the next question or complete the survey
                state.current_question += 1
                if state.current_question > len(survey_questions):  # Check if it's the last question
                    state.completed = True
                    await ChatbotService.save_conversation_state(conversation_id, state)
                    await websocket.send_text(
                        f"BOT: Thank you for your time, {customer_info['name']}! Your response has been recorded. Have a wonderful day!"
                    )
                    break

                # Save the updated state
                await ChatbotService.save_conversation_state(conversation_id, state)

        except WebSocketDisconnect:
            # Handle disconnection gracefully
            await ChatbotService.save_conversation_state(conversation_id, state)
            logger.info(f"WebSocket disconnected for customer {customer_id}")