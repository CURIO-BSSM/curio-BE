from fastapi import FastAPI
from app.core.config import engine, Base
import uvicorn

app = FastAPI(title="Science Project API")

from app.routers import quiz,auth,unit,rank
app.include_router(quiz.router)
app.include_router(auth.router)
app.include_router(unit.router)
app.include_router(rank.router)
# DB 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": ""}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
