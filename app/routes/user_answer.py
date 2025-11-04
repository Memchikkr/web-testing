from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from app.bearer import AccessController
from app.depends.uow import get_uow
from app.models.user import User, UserAnswer
from app.repositories.unit_of_work import SQLAlchemyUnitOfWork
from app.schemas.users import UserAnswerRequest, UserAnswerShort

router = APIRouter(
    prefix="/results",
    tags=["User Answers"],
    dependencies=[Depends(AccessController().get_access)],
)


@router.put("/{result_id}/answers", response_model=UserAnswerShort)
async def save_answer(
    request: UserAnswerRequest,
    current_user: Annotated[User, Depends(AccessController().get_access)],
    result_id: int = Path(ge=1),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    result = await uow.results.get(id=result_id, user_id=current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Запись о результатах не найдена")
    if result.finished_at is not None:
        raise HTTPException(status_code=403, detail="Прохождение теста завершено")

    user_answer = await uow.user_answers.get(
        result_id=result_id, question_id=request.question_id
    )

    question = await uow.questions.get(test_id=result.test_id, id=request.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    answer = await uow.answers.get(question_id=question.id)
    if not answer:
        raise HTTPException(status_code=404, detail="Ответа на данный вопрос нет")
    score = result.score if result.score else 0
    is_correct = False
    if answer.answer_text == request.answer_text:
        is_correct = True
        score = result.score + question.points if result.score else question.points
    if user_answer:
        if user_answer.is_correct == is_correct:
            score = result.score
        else:
            score = (
                result.score + question.points
                if is_correct is True
                else result.score - question.points
            )
        await uow.results.update(
            {"score": score},
            id=result.id,
        )
        await uow.user_answers.update(
            {"is_correct": is_correct, "answer_text": request.answer_text},
            result_id=user_answer.result_id,
            question_id=user_answer.question_id,
        )
        await uow.commit()
        return user_answer
    user_answer = UserAnswer(
        result_id=result_id,
        answer_id=answer.id,
        is_correct=is_correct,
        **request.model_dump(),
    )
    try:
        uow.user_answers.add(user_answer)
        await uow.results.update(
            {"score": score},
            id=result.id,
        )
        await uow.commit()
        return user_answer
    except Exception:
        raise HTTPException(
            status_code=422, detail="Произошла ошибка при сохранении ответа"
        )
