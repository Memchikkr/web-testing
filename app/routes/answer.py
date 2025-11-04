from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from app.bearer import AccessController
from app.models.answer import Answer
from app.models.user import User
from app.repositories import get_uow
from app.repositories.answer import AnswerRepository
from app.repositories.question import QuestionRepository
from app.repositories.testing import TestRepository
from app.repositories.unit_of_work import SQLAlchemyUnitOfWork
from app.schemas.answers import AnswerBase, AnswerCreateRequest
from app.utils.types import Role

router = APIRouter(
    prefix="/tests",
    tags=["Answers"],
    dependencies=[Depends(AccessController().get_access)],
)


@router.post("/{test_id}/questions/{question_id}/answers", response_model=AnswerBase)
async def create_answer(
    request: AnswerCreateRequest,
    current_user: Annotated[User, Depends(AccessController([Role.teacher]).get_access)],
    test_id: int = Path(ge=1),
    question_id: int = Path(ge=1),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    test_rep = TestRepository(uow.session)
    test = await test_rep.get(id=test_id, creator_id=current_user.id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    q_rep = QuestionRepository(uow.session)
    question = await q_rep.get(id=question_id, test_id=test_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    rep = AnswerRepository(uow.session)
    answer = await rep.get(question_id=question_id)
    if answer:
        raise HTTPException(status_code=409, detail="Ответ уже существует")
    answer = Answer(question_id=question_id, **request.model_dump())
    try:
        rep.add(answer)
        await uow.commit()
        return answer
    except Exception:
        raise HTTPException(
            status_code=422, detail="Произошла ошибка при создании ответа"
        )


@router.put(
    "/{test_id}/questions/{question_id}/answers/{answer_id}", response_model=AnswerBase
)
async def put_answer(
    request: AnswerCreateRequest,
    current_user: Annotated[User, Depends(AccessController([Role.teacher]).get_access)],
    test_id: int = Path(ge=1),
    question_id: int = Path(ge=1),
    answer_id: int = Path(ge=1),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):

    test_rep = TestRepository(uow.session)
    test = await test_rep.get(id=test_id, creator_id=current_user.id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    q_rep = QuestionRepository(uow.session)
    question = await q_rep.get(id=question_id, test_id=test_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    rep = AnswerRepository(uow.session)
    answer = await rep.get(id=answer_id, question_id=question_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Ответ не найден")
    try:
        await rep.update(request.model_dump(), id=answer_id)
        await uow.commit()
        return answer
    except Exception:
        raise HTTPException(
            status_code=422, detail="Произошла ошибка при обновлении ответа"
        )
