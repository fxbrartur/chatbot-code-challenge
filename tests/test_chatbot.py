from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_websocket_chatbot():
    with client.websocket_connect("/ws/1/ice_cream_preferences") as websocket:
        # Receive the first question
        data = websocket.receive_text()
        assert "Which flavor of ice cream do you prefer?" in data

        # Send a valid response (e.g., "2" for Chocolate)
        websocket.send_text("2")

        # Receive the next question
        data = websocket.receive_text()
        assert "Would you like to provide feedback on why you selected this flavor?" in data

        # Send a valid response (e.g., "2" for No)
        websocket.send_text("2")

        # Receive the completion message
        data = websocket.receive_text()
        assert "Thank you for your time, John Doe!" in data