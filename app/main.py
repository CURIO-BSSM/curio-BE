from fastapi import FastAPI
from app.core.config import engine, Base
from app.models import models

app = FastAPI(title="Science Project API")

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "DB 연동 테스트 성공!"}