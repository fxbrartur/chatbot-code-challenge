from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_websocket_chatbot():
    """Test the chatbot WebSocket endpoint."""
    with client.websocket_connect("/ws/1/ice_cream_preferences") as websocket:
        try:
            # Step 1: Receive the first message
            data = websocket.receive_text()

            # Normal flow: First question
            assert "Which flavor of ice cream do you prefer?" in data

            # Step 2: Send a valid response (e.g., "2" for Chocolate)
            websocket.send_text("2")

            # Step 3: Receive the next message
            data = websocket.receive_text()

            # Normal flow: Second question
            assert "Would you like to provide feedback on why you selected this flavor?" in data

            # Step 4: Send a valid response (e.g., "2" for No)
            websocket.send_text("2")

            # Step 5: Receive the completion message
            data = websocket.receive_text()

            # Normal flow: Completion message
            assert "Thank you for your time, John Doe!" in data

        except Exception as e:
            # If an unexpected error occurs, fail the test with the error message
            assert False, f"Unexpected error during test: {e}"