from sqlalchemy.orm import Session
from app.models.models import Unit, Question


def get_quiz_by_unit(db: Session, unit_id: int):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        return None

    questions = db.query(Question).filter(Question.unit_id == unit_id).all()
    return {"unit": unit, "questions": questions}