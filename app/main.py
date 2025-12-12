from fastapi import FastAPI
from app.core.config import engine, Base
import uvicorn


app = FastAPI(title="Science Project API")

from fastapi.middleware.cors import CORSMiddleware
origins= [
    "http://localhost:5173",
]

origins = [
    "http://localhost:5173",
    "https://curio-fe.vercel.app",
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 개발 중엔 * 로 두고, 배포 시 특정 도메인만
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import quiz,auth,unit,rank,history
app.include_router(quiz.router)
app.include_router(auth.router)
app.include_router(unit.router)
app.include_router(rank.router)
app.include_router(history.router)
# DB 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": ""}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
