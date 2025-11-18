from app.models.models import History, Unit
from sqlalchemy.orm import Session
from datetime import datetime, timezone

def create_user_history(db: Session, user_id: int, unit_id: int, score: int):
    history = History(
        user_id=user_id,
        unit_id=unit_id,
        score=score,
        answered_at=datetime.now(timezone.utc)
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

def get_user_history(db: Session, user_id: int):
    result = (
        db.query(History, Unit.name.label("unit_name"))
        .join(Unit, History.unit_id == Unit.id)
        .filter(History.user_id == user_id)
        .order_by(History.answered_at.desc())
        .all()
    )

    history_list = []
    for history, unit_name in result:
        history_list.append({
            "id": history.id,
            "user_id": history.user_id,
            "unit_name": unit_name,
            "score": history.score,
            "answered_at": history.answered_at,
        })
    return history_list
