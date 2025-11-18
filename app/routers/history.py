from fastapi import APIRouter, Depends, HTTPException, status
from app.crud.history_crud import get_user_history, create_user_history
from app.schemas.history_schemas import History
from app.core.config import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["History"])

@router.get("/{user_id}/history", response_model=list[History])
def read_history(user_id: int, db: Session = Depends(get_db)):
    histories = get_user_history(db, user_id=user_id)
    if not histories:
        raise HTTPException(status_code=404, detail="사용자 이력이 존재하지 않습니다.")
    return histories