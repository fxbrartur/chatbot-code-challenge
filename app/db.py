import time
import random
from typing import Dict, Any, Optional

mock_db = {
    "conversations": {},
    "customers": {
        "1": {"name": "John Doe", "email": "john.doe@example.com"},
        "2": {"name": "Jane Smith", "email": "jane.smith@example.com"},
    },
    "surveys": []
}

# Simulate network latency and possible failures
def simulate_rpc_call():
    time.sleep(random.uniform(0.1, 0.5))  # Simulate network delay
    if random.random() < 0.1:  # 10% chance of failure
        raise ConnectionError("RPC call failed")


class MockRPCDatabase:
    """
    An example mock database.
    Adjust and customize this file as you wish, but assume all db access is via RPCs.
    """
    @staticmethod
    def get_conversation_state(conversation_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the state of a conversation."""
        simulate_rpc_call()
        return mock_db["conversations"].get(conversation_id)

    @staticmethod
    def save_conversation_state(conversation_id: str, state: Dict[str, Any]) -> None:
        """Save or update the state of a conversation."""
        simulate_rpc_call()
        mock_db["conversations"][conversation_id] = state

    @staticmethod
    def get_customer_info(customer_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve customer information."""
        simulate_rpc_call()
        return mock_db["customers"].get(customer_id)

    @staticmethod
    def save_survey_response(response: Dict[str, Any]) -> None:
        """Save a survey response."""
        simulate_rpc_call()
        mock_db["surveys"].append(response)


# Example usage (commented out, meant for testing)
# if __name__ == "__main__":
#     db = MockRPCDatabase()
#     print("Fetching customer info:", db.get_customer_info("1"))
#     db.save_conversation_state("conv123", {"messages": ["Hi!", "Hello!"]})
#     print("Conversation state:", db.get_conversation_state("conv123"))
#     db.save_survey_response({"customer_id": "1", "feedback": "Great service!"})
#     print("Surveys:", mock_db["surveys"])
