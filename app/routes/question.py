from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from app.bearer import AccessController
from app.models.question import Question
from app.models.user import User
from app.repositories import get_uow
from app.repositories.question import QuestionRepository
from app.repositories.testing import TestRepository
from app.repositories.unit_of_work import SQLAlchemyUnitOfWork
from app.schemas.questions import QuestionCreateRequest, QuestionBase
from app.utils.types import Role

router = APIRouter(
    prefix="/tests",
    tags=["Questions"],
    dependencies=[Depends(AccessController().get_access)],
)


@router.post("/{test_id}/questions", response_model=QuestionBase)
async def create_question(
    request: QuestionCreateRequest,
    current_user: Annotated[User, Depends(AccessController([Role.teacher]).get_access)],
    test_id: int = Path(ge=1),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    
    test_rep = TestRepository(uow.session)
    test = await test_rep.get(id=test_id, creator_id=current_user.id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    rep = QuestionRepository(uow.session)
    question = Question(test_id=test_id, **request.model_dump())
    try:
        rep.add(question)
        await uow.commit()
        return question
    except Exception:
        raise HTTPException(
            status_code=422, detail="Произошла ошибка при создании вопроса"
        )


@router.put("/{test_id}/questions/{question_id}", response_model=QuestionBase)
async def put_question(
    request: QuestionCreateRequest,
    current_user: Annotated[User, Depends(AccessController([Role.teacher]).get_access)],
    test_id: int = Path(ge=1),
    question_id: int = Path(ge=1),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    
    test_rep = TestRepository(uow.session)
    test = await test_rep.get(id=test_id, creator_id=current_user.id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    rep = QuestionRepository(uow.session)
    question = await rep.get(id=question_id, test_id=test_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    try:
        await rep.update(request.model_dump(), id=question_id)
        await uow.commit()
        return question
    except Exception:
        raise HTTPException(
            status_code=422, detail="Произошла обновлении вопроса"
        )
