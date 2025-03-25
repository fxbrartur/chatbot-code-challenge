from typing import Dict, List, Optional
from app.models.models import SurveyQuestion

# Define the surveys
SURVEYS = {
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
    "cake_preferences": {
        "id": "cake_preferences",
        "title": "Cake Preferences Survey",
        "questions": [
            {
                "id": 1,
                "question": "Which type of cake do you prefer?",
                "options": ["Carrot Cake", "Tiramisu Cake", "Red Velvet"]
            },
            {
                "id": 2,
                "question": "Would you like to provide feedback on why you selected this flavor?",
                "options": ["Yes", "No"]
            }
        ]
    },
    "beer_preferences": {
        "id": "beer_preferences",
        "title": "Beer Preferences Survey",
        "questions": [
            {
                "id": 1,
                "question": "Which type of beer do you prefer?",
                "options": ["IPA", "Stout", "Lager"]
            },
            {
                "id": 2,
                "question": "Would you like to provide feedback on why you selected this flavor?",
                "options": ["Yes", "No"]
            }
        ]
    }
}

def get_survey_questions(survey_id: str) -> Optional[List[SurveyQuestion]]:
    """Retrieve questions for a specific survey."""
    survey = SURVEYS.get(survey_id)
    if not survey:
        return None
    return [SurveyQuestion(**q) for q in survey["questions"]]

def get_survey_info(survey_id: str) -> Optional[Dict[str, any]]:
    """Retrieve survey information."""
    return SURVEYS.get(survey_id)