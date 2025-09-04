from sqlalchemy.orm import Session
from app.models.models import Unit

def get_unit(db: Session, unit_id: int):
    unit = db.query(Unit).filter(Unit.id == unit_id).all
    if not unit:
        return None
    return unit