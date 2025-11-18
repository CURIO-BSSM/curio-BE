from fastapi import APIRouter, Depends, HTTPException, Query,status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.crud.ranking_crud import update_score
from app.core.security import admin_required
from app.crud.question_crud import get_quiz_by_unit, get_question_by_id, save_user_answers_bulk, save_new_quiz
from app.schemas.question_schemas import QuizOut, QuestionOut, QuizRequest,QuizResponse,QuizAdd, QuizAddResponse
from app.core.config import get_db
from app.crud.history_crud import create_user_history

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
            options=q.options,
            correct_answer = q.correct_answer,
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

    score = len(correct)
    update_score(db, request.user_id, score)
    create_user_history(db, user_id=request.user_id, unit_id=request.unit_id, score=score)

    return QuizResponse(
        score=score,
        total=len(request.answers),
        correct=correct,
        wrong=wrong
    )
@router.post("/add", response_model=QuizAddResponse)
def add_quiz(request: QuizAdd, db: Session = Depends(get_db),current_user=Depends(admin_required)):
    if request.question_type not in ["objective", "subjective"]:
        raise HTTPException(status_code=400, detail="문항 유형은 객관식 또는 주관식만 가능합니다.")

    addedQuiz = {
        "unit_id": request.unit_id,
        "content": request.content,
        "options": request.options,
        "question_type": request.question_type,
        "correct_answer": request.correct_answer,
    }

    Quiz = save_new_quiz(db, addedQuiz)
    return QuizAddResponse(message="퀴즈가 성공적으로 추가되었습니다.", questions_id=Quiz.id)
