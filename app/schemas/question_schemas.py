from pydantic import BaseModel
from typing import List

class QuestionOut(BaseModel):
    id: int
    content: str
    options: List[str]

class QuizOut(BaseModel):
    unit_id: int
    unit_name: str
    questions: List[QuestionOut]
    model_config = {"from_attributes": True}