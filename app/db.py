import time
import random
from typing import Dict, Any, Optional, List
from app.models.models import SurveyQuestion
from app.utils.surveys import get_survey_questions, get_survey_info

mock_db = {
    "conversations": {},
    "customers": {
        "1": {"name": "John Doe", "email": "john.doe@example.com"},
        "2": {"name": "Jane Smith", "email": "jane.smith@example.com"},
    },
    "survey_responses": []
}

class MockRPCDatabase:
    """Mock database with RPC-like behavior."""

    @staticmethod
    def simulate_rpc_call():
        """Simulate network latency and possible failures."""
        time.sleep(random.uniform(0.1, 0.5))
        if random.random() < 0.1:  # 10% chance of failure
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
        return get_survey_questions(survey_id)  

    def get_survey_info(self, survey_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve survey information."""
        self.simulate_rpc_call()
        return get_survey_info(survey_id)  