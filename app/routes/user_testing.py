from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path

from app.bearer import AccessController
from app.models.testing import Test
from app.models.user import User
from app.repositories import get_uow
from app.repositories.testing import TestRepository
from app.repositories.unit_of_work import SQLAlchemyUnitOfWork
from app.schemas.tests import TestBase, TestCreateRequest, TestWithQuestionsAndAnswers
from app.utils.types import Role

router = APIRouter(
    prefix="/users/tests",
    tags=["User Tests"],
    dependencies=[Depends(AccessController().get_access)],
)


@router.post("", response_model=TestBase)
async def create_test(
    request: TestCreateRequest,
    current_user: Annotated[User, Depends(AccessController([Role.teacher]).get_access)],
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    try:
        rep = TestRepository(uow.session)
        test = Test(creator_id=current_user.id, **request.model_dump())
        rep.add(test)
        await uow.commit()
        return test
    except Exception:
        raise HTTPException(
            status_code=422, detail="Произошла ошибка при создании теста"
        )


@router.get("", response_model=List[TestBase])
async def get_my_tests(
    current_user: Annotated[User, Depends(AccessController([Role.teacher]).get_access)],
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    try:
        rep = TestRepository(uow.session)
        tests = await rep.get_all_by_conditions(creator_id=current_user.id)
        return tests
    except Exception:
        raise HTTPException(
            status_code=422, detail="Произошла ошибка при получении тестов"
        )


@router.get("/{test_id}", response_model=TestWithQuestionsAndAnswers)
async def get_my_test(
    current_user: Annotated[User, Depends(AccessController([Role.teacher]).get_access)],
    test_id: int = Path(ge=1),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    rep = TestRepository(uow.session)
    test = await rep.get_test_with_questions_and_answers(
        id=test_id, creator_id=current_user.id
    )
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    return test
