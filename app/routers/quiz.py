from fastapi import APIRouter, Depends, HTTPException, Query,status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.crud.question_crud import get_quiz_by_unit, get_question_by_id, save_user_answers_bulk, save_new_quiz
from app.schemas.question_schemas import QuizOut, QuestionOut, QuizRequest,QuizResponse,QuizAdd
from app.core.config import get_db

router = APIRouter(prefix="/quiz" ,tags=["quiz"])


@router.get("/", response_model=QuizOut)
# int = Query(...)은 쿼리 파라미터로 받겠다는 거임
def get_quiz(unit_id: int = Query(...), db: Session = Depends(get_db)):
    result = get_quiz_by_unit(db, unit_id)
    if not result:
        raise HTTPException(status_code=404, detail="해당 단원에 대한 퀴즈를 찾을 수 없습니다.")
    unit = result["unit"]
    questions = [
        QuestionOut(
            id=q.id,
            content=q.content,
            options=q.options
        ) for q in result["questions"]
    ]

    return QuizOut(
        unit_id=unit.id,
        unit_name=unit.name,
        questions=questions
    )

@router.post("/submit", response_model=QuizResponse)
def submit_quiz(request: QuizRequest, db: Session = Depends(get_db)):
    correct = []
    wrong = []
    user_answers_bulk = []

    for ans in request.answers:
        question = get_question_by_id(db, ans.question_id)
        if not question:
            wrong.append(ans.question_id)
            continue

        is_correct = str(ans.selected_answer) == str(question.correct_answer)
        if is_correct:
            correct.append(ans.question_id)
        else:
            wrong.append(ans.question_id)

        user_answers_bulk.append({
            "user_id": request.user_id,
            "question_id": ans.question_id,
            "selected_answer": ans.selected_answer,
            "is_correct": is_correct
        })

    if user_answers_bulk:
        save_user_answers_bulk(db, user_answers_bulk)

    return QuizResponse(
        score=len(correct),
        total=len(request.answers),
        correct=correct,
        wrong=wrong
    )
@router.post("/add", response_model=QuizAdd)
def add_quiz(request: QuizAdd, db: Session = Depends(get_db)):
    addedQuiz = {
        "unit_id": request.unit_id,
        "content": request.content,
        "options": request.options,
        "correct_answer": request.correct_answer,
    }
    if addedQuiz:
        Quiz = save_new_quiz(db, addedQuiz)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "퀴즈가 성공적으로 추가되었습니다.","questions_id":Quiz.questions_id}
    )