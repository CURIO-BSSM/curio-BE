from sqlalchemy.orm import Session
from app.models.models import Unit

def get_unit(db: Session):
    unit = db.query(Unit).all()
    if not unit:
        return None
    return unit # 리스트로 반환
