from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.unit_crud import get_unit
from app.schemas.unit_schemas import units
from app.core.config import get_db

router = APIRouter(prefix="/units", tags=["units"])

@router.get("/", response_model=list[units])
def read_unit(db: Session = Depends(get_db)):
    result = get_unit(db)
    if not result:
        raise HTTPException(status_code=404, detail="단원 목록을 불러오는 데 실패했습니다.")
    return result