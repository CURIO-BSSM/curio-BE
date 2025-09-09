from sqlalchemy.orm import Session
from app.models.models import Unit, Question,UserAnswer
from datetime import datetime,timezone


def get_quiz_by_unit(db: Session, unit_id: int):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        return None
    questions = db.query(Question).filter(Question.unit_id == unit_id).all()
    return {"unit": unit, "questions": questions}

def get_question_by_id(db: Session, question_id: int):
    return db.query(Question).filter(Question.id == question_id).first()

def save_user_answer(db: Session, user_id: int, question_id: int, selected_answer: str, is_correct: bool):
    ua = UserAnswer(
        user_id=user_id,
        question_id=question_id,
        selected_answer=selected_answer,
        is_correct=is_correct,
        answered_at=datetime.now(timezone.utc)
    )
    db.add(ua)
    db.commit()
    db.refresh(ua)
    return ua


def save_user_answers_bulk(db: Session, answers: list):
    user_answers = [
        UserAnswer(
            user_id=a["user_id"],
            question_id=a["question_id"],
            selected_answer=a["selected_answer"],
            is_correct=a["is_correct"],
            answered_at=datetime.now(timezone.utc)
        ) for a in answers
    ]
    db.add_all(user_answers)
    db.commit()
    return user_answers