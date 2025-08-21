from fastapi import FastAPI
from app.core.config import engine, Base

app = FastAPI(title="Science Project API")

from app.routers import quiz,auth
app.include_router(quiz.router)
app.include_router(auth.router)
# DB 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": ""}