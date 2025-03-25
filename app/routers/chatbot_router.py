from fastapi import APIRouter, WebSocket
from app.services.chatbot_service import ChatbotService

router = APIRouter()

@router.websocket("/ws/{customer_id}/{survey_id}")
async def chatbot_websocket(websocket: WebSocket, customer_id: str, survey_id: str):
    """WebSocket endpoint for the chatbot."""
    await ChatbotService.handle_websocket_interaction(websocket, customer_id, survey_id)