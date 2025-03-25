from app.models.models import SurveyQuestion
from app.routers.chatbot_router import SURVEY_QUESTIONS

class SurveyService:
    @staticmethod
    def get_next_question(question_id: int) -> SurveyQuestion:
        """Retrieve the next question based on the current question ID."""
        # For now, return the next question in sequence
        return SURVEY_QUESTIONS[question_id - 1]