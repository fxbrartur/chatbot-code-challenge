from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.models import SurveyQuestion, SurveyResponse, ConversationState
from app.db import MockRPCDatabase

router = APIRouter()
db = MockRPCDatabase()

# Predefined survey questions
SURVEY_QUESTIONS = [
    SurveyQuestion(id=1, question="Which flavor of ice cream do you prefer?", options=["Vanilla", "Chocolate", "Strawberry"]),
    SurveyQuestion(id=2, question="Would you like to provide feedback on why you selected this flavor?", options=["Yes", "No"]),
]

@router.websocket("/ws/{customer_id}")
async def chatbot_websocket(websocket: WebSocket, customer_id: str):
    """WebSocket endpoint for the chatbot."""
    await websocket.accept()

    # Retrieve customer info
    customer_info = db.get_customer_info(customer_id)
    if not customer_info:
        await websocket.send_text("Customer not found.")
        await websocket.close()
        return

    # Initialize or retrieve conversation state
    conversation_id = f"conv_{customer_id}"
    state_data = db.get_conversation_state(conversation_id)
    if state_data:
        state = ConversationState(**state_data)
    else:
        state = ConversationState(customer_id=customer_id, current_question=1, completed=False, responses=[])
        db.save_conversation_state(conversation_id, state.model_dump())

    try:
        while not state.completed:
            # Send the current question
            question = SURVEY_QUESTIONS[state.current_question - 1]
            await websocket.send_json({"question": question.model_dump()})

            # Receive the customer's response
            response_data = await websocket.receive_json()
            response = SurveyResponse(**response_data)

            # Save the response
            state.responses.append(response)
            db.save_survey_response(response.model_dump())

            # Move to the next question or complete the survey
            state.current_question += 1
            if state.current_question > len(SURVEY_QUESTIONS):
                state.completed = True
                db.save_conversation_state(conversation_id, state.model_dump())
                await websocket.send_text("Thank you for completing the survey!")
                break

            # Save the updated state
            db.save_conversation_state(conversation_id, state.model_dump())

    except WebSocketDisconnect:
        # Handle disconnection gracefully
        db.save_conversation_state(conversation_id, state.model_dump())
        print(f"WebSocket disconnected for customer {customer_id}")