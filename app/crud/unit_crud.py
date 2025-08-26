from app.models.models import Unit
from sqlalchemy.orm import Session

def get_unit(db: Session):
    return db.query(Unit).order_by(Unit.id).all()