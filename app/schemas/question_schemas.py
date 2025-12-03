from pydantic import BaseModel
from typing import List

class QuestionOut(BaseModel):
    id: int
    content: str
    options: List[str]
    correct_answer : int

class QuizOut(BaseModel):
    unit_id: int
    unit_name: str
    questions: List[QuestionOut]
    model_config = {"from_attributes": True}

class Answer(BaseModel):
    question_id: int
    selected_answer: int

class QuizRequest(BaseModel):
    user_id: int
    unit_id: int
    answers: List[Answer]

class QuizResponse(BaseModel):
    score: int
    total: int
    correct: List[int]
    wrong: List[int]

class QuizAdd(BaseModel):
    unit_id: int
    content: str
    options: List[str]
    correct_answer: int