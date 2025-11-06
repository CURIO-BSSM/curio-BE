from app.models.models import Ranking
from sqlalchemy.orm import Session

def rankings(db: Session, limit: int = 100):
    return (
        db.query(Ranking)
        .order_by(Ranking.score.desc())
        .limit(limit)
        .all()
    )