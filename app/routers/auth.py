from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate, Token, UserLogin, UserLogout
from app.core.config import get_db
from app.models.models import User
from app.core.security import create_access_token,hash_password,verify_password

router = APIRouter(prefix="/auth" ,tags=["auth"])

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일 입니다.")

    new_user = User(name=user.name, password_hash=hash_password(user.password),email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    exp,access_token = create_access_token({"sub": new_user.email})
    return {"message": "회원가입이 완료되었습니다.", "user_id": new_user.id,"access_token": access_token, "token_type": "bearer", "expires_in": exp.isoformat()}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    exp,access_token = create_access_token({"sub": db_user.email})

    return {"access_token": access_token, "token_type": "bearer", "expires_in": exp.isoformat() }

@router.post("/logout")
def logout():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "로그아웃이 완료되었습니다."}
    )
