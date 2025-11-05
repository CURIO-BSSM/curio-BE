from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.crud.ranking_crud import rankings
from app.schemas.ranking_schemas import Ranking

router = APIRouter(prefix="/rankings", tags=["Rankings"])

@router.get("/", response_model=list[Ranking])
def get_rankings(db: Session = Depends(get_db)):
    ranks = rankings(db)
    if not ranks:
        raise HTTPException(status_code=404, detail="랭킹 정보를 불러오는 데 실패했습니다.")
    return ranks