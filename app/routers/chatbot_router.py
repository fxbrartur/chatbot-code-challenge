from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.models import SurveyResponse, ConversationState
from app.db import MockRPCDatabase
import logging

router = APIRouter()
db = MockRPCDatabase()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Centralized error message
TECHNICAL_DIFFICULTIES_MESSAGE = "We are experiencing technical difficulties. Please try again later."

@router.websocket("/ws/{customer_id}/{survey_id}")
async def chatbot_websocket(
    websocket: WebSocket,
    customer_id: str,
    survey_id: str
):
    """WebSocket endpoint for the chatbot."""
    await websocket.accept()

    # Retrieve customer info with error handling
    try:
        customer_info = db.get_customer_info(customer_id)
        if not customer_info:
            await websocket.send_text("Customer not found.")
            await websocket.close()
            return
    except ConnectionError:
        await websocket.send_text(TECHNICAL_DIFFICULTIES_MESSAGE)
        await websocket.close()
        return

    # Retrieve survey questions with error handling
    try:
        survey_questions = db.get_survey_questions(survey_id)
        if not survey_questions:
            await websocket.send_text("Survey not found.")
            await websocket.close()
            return
    except ConnectionError:
        await websocket.send_text(TECHNICAL_DIFFICULTIES_MESSAGE)
        await websocket.close()
        return

    # Initialize or retrieve conversation state
    conversation_id = f"conv_{customer_id}_{survey_id}"
    try:
        state_data = db.get_conversation_state(conversation_id)
        if state_data:
            state = ConversationState(**state_data)
        else:
            state = ConversationState(
                customer_id=customer_id,
                current_question=1,
                completed=False,
                responses=[],
                survey_id=survey_id
            )
            db.save_conversation_state(conversation_id, state.model_dump())
    except ConnectionError:
        await websocket.send_text(TECHNICAL_DIFFICULTIES_MESSAGE)
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
                    answer=feedback
                )
            else:
                try:
                    response_index = int(response_data) - 1
                    if response_index < 0 or response_index >= len(options):
                        raise ValueError
                    response = SurveyResponse(
                        customer_id=customer_id,
                        question_id=question.id,
                        answer=options[response_index]
                    )
                except ValueError:
                    await websocket.send_text(
                        "BOT: Invalid response. Please reply with the number corresponding to your choice."
                    )
                    continue

            # Save the response with error handling
            try:
                state.responses.append(response)
                db.save_survey_response(response.model_dump())
            except ConnectionError:
                await websocket.send_text(TECHNICAL_DIFFICULTIES_MESSAGE)
                await websocket.close()
                return

            # Move to the next question or complete the survey
            state.current_question += 1
            if state.current_question > len(survey_questions):  # Check if it's the last question
                state.completed = True
                try:
                    db.save_conversation_state(conversation_id, state.model_dump())
                except ConnectionError:
                    await websocket.send_text(TECHNICAL_DIFFICULTIES_MESSAGE)
                    await websocket.close()
                    return
                await websocket.send_text(
                    f"BOT: Thank you for your time, {customer_info['name']}! Your response has been recorded. Have a wonderful day!"
                )
                break

            # Save the updated state with error handling
            try:
                db.save_conversation_state(conversation_id, state.model_dump())
            except ConnectionError:
                await websocket.send_text(TECHNICAL_DIFFICULTIES_MESSAGE)
                await websocket.close()
                return

    except WebSocketDisconnect:
        # Handle disconnection gracefully
        try:
            db.save_conversation_state(conversation_id, state.model_dump())
        except ConnectionError:
            logger.warning(f"Failed to save conversation state for customer {customer_id} after disconnection.")
        print(f"WebSocket disconnected for customer {customer_id}")