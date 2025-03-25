from app.models.models import SurveyQuestion
from app.db import MockRPCDatabase
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SurveyService:
    def __init__(self):
        self.db = MockRPCDatabase()

    def get_next_question(self, survey_id: str, question_id: int) -> SurveyQuestion:
        """
        Retrieve the next question based on the current question ID.
        Includes error handling for RPC failures.
        """
        retries = 3  # Number of retries for RPC calls
        for attempt in range(retries):
            try:
                # Attempt to retrieve survey questions
                questions = self.db.get_survey_questions(survey_id)
                if not questions:
                    raise ValueError(f"Survey with ID '{survey_id}' not found.")

                # Return the next question in sequence
                return questions[question_id - 1]
            except ConnectionError as e:
                logger.warning(f"RPC call failed on attempt {attempt + 1}/{retries}: {e}")
                if attempt == retries - 1:
                    # If all retries fail, log the error and raise an exception
                    logger.error(f"All RPC retries failed for survey_id '{survey_id}'.")
                    raise ConnectionError("Unable to retrieve survey questions due to repeated RPC failures.")
            except IndexError:
                # Handle invalid question ID
                logger.error(f"Invalid question ID '{question_id}' for survey '{survey_id}'.")
                raise ValueError(f"Question ID '{question_id}' is out of range for survey '{survey_id}'.")
            except Exception as e:
                # Handle unexpected errors
                logger.error(f"Unexpected error while retrieving question: {e}")
                raise

    def save_survey_response(self, response: dict) -> None:
        """
        Save a survey response with error handling for RPC failures.
        """
        retries = 3  # Number of retries for RPC calls
        for attempt in range(retries):
            try:
                self.db.save_survey_response(response)
                return  # Exit if successful
            except ConnectionError as e:
                logger.warning(f"RPC call failed on attempt {attempt + 1}/{retries}: {e}")
                if attempt == retries - 1:
                    # If all retries fail, log the error and raise an exception
                    logger.error(f"All RPC retries failed while saving response: {response}")
                    raise ConnectionError("Unable to save survey response due to repeated RPC failures.")
            except Exception as e:
                # Handle unexpected errors
                logger.error(f"Unexpected error while saving response: {e}")
                raise