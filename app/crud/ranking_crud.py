from app.models.models import Ranking, User
from sqlalchemy.orm import Session

def rankings(db: Session, limit: int = 100):
    result = (
        db.query(Ranking, User.name)
        .join(User, Ranking.user_id == User.id)
        .order_by(Ranking.score.desc())
        .limit(limit)
        .all()
    )
    ranking_list = []
    for idx, (ranking, username) in enumerate(result, start=1):
        ranking_list.append({
            "rank": idx,
            "username": username,
            "user_id": ranking.user_id,
            "score": ranking.score,
        })
    return ranking_list

def update_score(db: Session, user_id: int, score: int):
    ranking = db.query(Ranking).filter(Ranking.user_id == user_id).first()
    if ranking:
        if score > ranking.score:
            ranking.score = score
    else:
        ranking = Ranking(user_id=user_id, score=score)
        db.add(ranking)

    db.commit()
    db.refresh(ranking)
    return ranking