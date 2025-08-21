# routers/quiz.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud.question_crud import get_quiz_by_unit
from app.schemas.question_schemas import QuizOut, QuestionOut
from app.core.config import SessionLocal

router = APIRouter(prefix="/quiz", tags=["Quiz"])


# DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=QuizOut)
# int = Query(...)은 쿼리 파라미터로 받겠다는 거임
def get_quiz(unit_id: int = Query(...), db: Session = Depends(get_db)):
    result = get_quiz_by_unit(db, unit_id)
    if not result:
        raise HTTPException(status_code=404, detail="해당 단원에 대한 퀴즈를 찾을 수 없습니다.")
    unit = result["unit"]
    questions = [
        QuestionOut(
            id=q.id,
            content=q.content,
            options=q.options
        ) for q in result["questions"]
    ]

    return QuizOut(
        unit_id=unit.id,
        unit_name=unit.name,
        questions=questions
    )