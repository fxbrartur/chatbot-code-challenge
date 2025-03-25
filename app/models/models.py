from pydantic import BaseModel
from typing import List, Optional

class SurveyQuestion(BaseModel):
    id: int
    question: str
    options: List[str]

class SurveyResponse(BaseModel):
    customer_id: str
    question_id: int
    answer: str

class ConversationState(BaseModel):
    customer_id: str
    current_question: Optional[int] = None
    completed: bool = False
    responses: List[SurveyResponse] = []