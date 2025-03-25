from app.models import ConversationState, SurveyResponse

class StateManager:
    @staticmethod
    def initialize_state(customer_id: str) -> ConversationState:
        """Initialize a new conversation state."""
        return ConversationState(customer_id=customer_id, current_question=1, completed=False, responses=[])

    @staticmethod
    def update_state(state: ConversationState, response: SurveyResponse) -> ConversationState:
        """Update the state with a new response."""
        state.responses.append(response)
        state.current_question += 1
        return state