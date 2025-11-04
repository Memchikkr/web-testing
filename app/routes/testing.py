from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.bearer import AccessController
from app.depends.uow import get_uow
from app.models.user import User
from app.repositories.unit_of_work import SQLAlchemyUnitOfWork
from app.schemas.tests import TestBase, TestWithQuestions

router = APIRouter(
    prefix="/tests",
    tags=["Tests"],
    dependencies=[Depends(AccessController().get_access)],
)


@router.get("/{test_id}", response_model=TestWithQuestions)
async def get_test(
    current_user: Annotated[User, Depends(AccessController().get_access)],
    test_id: int = Path(ge=1),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    test = await uow.tests.get_test_with_questions(id=test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    return test


@router.get("", response_model=List[TestBase])
async def get_tests(
    current_user: Annotated[User, Depends(AccessController().get_access)],
    filter: str | None = Query(default=None),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    try:
        tests = await uow.tests.search_tests(filter=filter)
        return tests
    except Exception:
        raise HTTPException(
            status_code=422, detail="Произошла ошибка при получении тестов"
        )
