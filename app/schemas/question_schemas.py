from pydantic import BaseModel
from typing import List, Optional, Dict

class QuestionOut(BaseModel):
    id: int
    content: str
    question_type: str
    options: Optional[Dict[str, str]] = None # 객관식만

class QuizOut(BaseModel):
    unit_id: int
    unit_name: str
    questions: List[QuestionOut]
    model_config = {"from_attributes": True}

class Answer(BaseModel):
    question_id: int
    selected_answer: str
    # 객관식과 주관식 모두 자연스러운 처리를 위해 str로 바꿈

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
    question_type: str
    options: Optional[Dict[str, str]] = None  # 객관식만
    correct_answer: str


class QuizAddResponse(BaseModel):
    message: str
    questions_id: int
