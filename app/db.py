import time
import random
from typing import Dict, Any, Optional, List
from app.models.models import SurveyQuestion

mock_db = {
    "conversations": {},
    "customers": {
        "1": {"name": "John Doe", "email": "john.doe@example.com"},
        "2": {"name": "Jane Smith", "email": "jane.smith@example.com"},
    },
    "surveys": {
        "ice_cream_preferences": {
            "id": "ice_cream_preferences",
            "title": "Ice Cream Preferences Survey",
            "questions": [
                {
                    "id": 1,
                    "question": "Which flavor of ice cream do you prefer?",
                    "options": ["Vanilla", "Chocolate", "Strawberry"]
                },
                {
                    "id": 2,
                    "question": "Would you like to provide feedback on why you selected this flavor?",
                    "options": ["Yes", "No"]
                }
            ]
        },
        "customer_satisfaction": {
            "id": "customer_satisfaction",
            "title": "Customer Satisfaction Survey",
            "questions": [
                {
                    "id": 1,
                    "question": "How would you rate our service?",
                    "options": ["Excellent", "Good", "Fair", "Poor"]
                },
                {
                    "id": 2,
                    "question": "Would you recommend us to a friend?",
                    "options": ["Yes", "Maybe", "No"]
                }
            ]
        }
    },
    "survey_responses": []
}

class MockRPCDatabase:
    """Mock database with RPC-like behavior."""

    @staticmethod
    def simulate_rpc_call():
        """Simulate network latency and possible failures."""
        time.sleep(random.uniform(0.1, 0.5))
        if random.random() < 0.1:
            raise ConnectionError("RPC call failed")

    def get_conversation_state(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the state of a conversation."""
        self.simulate_rpc_call()
        return mock_db["conversations"].get(conversation_id)

    def save_conversation_state(self, conversation_id: str, state: Dict[str, Any]) -> None:
        """Save or update the state of a conversation."""
        self.simulate_rpc_call()
        mock_db["conversations"][conversation_id] = state

    def get_customer_info(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve customer information."""
        self.simulate_rpc_call()
        return mock_db["customers"].get(customer_id)

    def save_survey_response(self, response: Dict[str, Any]) -> None:
        """Save a survey response."""
        self.simulate_rpc_call()
        mock_db["survey_responses"].append(response)

    def get_survey_questions(self, survey_id: str) -> Optional[List[SurveyQuestion]]:
        """Retrieve questions for a specific survey."""
        self.simulate_rpc_call()
        survey = mock_db["surveys"].get(survey_id)
        if not survey:
            return None

        return [SurveyQuestion(**q) for q in survey["questions"]]

    def get_survey_info(self, survey_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve survey information."""
        self.simulate_rpc_call()
        return mock_db["surveys"].get(survey_id)