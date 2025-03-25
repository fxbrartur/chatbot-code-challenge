from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_websocket_chatbot():
    with client.websocket_connect("ws/1/ice_cream_preferences") as websocket:
        # Receive the first question
        data = websocket.receive_json()
        assert data["question"]["id"] == 1

        # Send a response
        websocket.send_json({"customer_id": "1", "question_id": 1, "answer": "Chocolate"})

        # Receive the next question
        data = websocket.receive_json()
        assert data["question"]["id"] == 2

        # Send another response
        websocket.send_json({"customer_id": "1", "question_id": 2, "answer": "No"})

        # Receive the completion message
        data = websocket.receive_text()
        assert "Thank you for completing the survey!" in data