from datetime import UTC, datetime, timedelta
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path

from app.bearer import AccessController
from app.depends.uow import get_uow
from app.models.user import Result, User
from app.repositories.unit_of_work import SQLAlchemyUnitOfWork
from app.schemas.results import ResultBase, ResultWithTest, ResultWithTestAndAnswers

router = APIRouter(
    prefix="/results",
    tags=["Results"],
    dependencies=[Depends(AccessController().get_access)],
)


@router.post("/tests/{test_id}", response_model=ResultBase)
async def start_test(
    current_user: Annotated[User, Depends(AccessController().get_access)],
    test_id: int = Path(ge=1),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    test = await uow.tests.get_test_with_questions(id=test_id)
    if not test:
        raise HTTPException(status_code=422, detail="Тест не найден")
    result = Result(user_id=current_user.id, test_id=test_id)
    try:
        uow.results.add(result)
        await uow.commit()
        return result
    except Exception:
        raise HTTPException(
            status_code=422, detail="Произошла ошибка при старте тестирования"
        )


@router.patch("/{result_id}", response_model=ResultWithTestAndAnswers)
async def finish_test(
    current_user: Annotated[User, Depends(AccessController().get_access)],
    result_id: int = Path(ge=1),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    result = await uow.results.get_result_with_test_and_answers(
        id=result_id, user_id=current_user.id
    )
    if not result:
        raise HTTPException(status_code=422, detail="Результат не найден")
    if result.finished_at:
        raise HTTPException(status_code=409, detail="Тест уже завершён")
    test = await uow.tests.get(id=result.test_id)
    if not test:
        raise HTTPException(status_code=422, detail="Тест не найден")
    now = datetime.now(UTC).replace(tzinfo=None)
    values = {"finished_at": now}
    if now - result.started_at > timedelta(minutes=test.time_limit_minutes):
        values["score"] = 0
    await uow.results.update(values, id=result_id)
    await uow.commit()
    return result


@router.get("/{result_id}", response_model=ResultWithTestAndAnswers)
async def get_result(
    current_user: Annotated[User, Depends(AccessController().get_access)],
    result_id: int = Path(ge=1),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    result = await uow.results.get_result_with_test_and_answers(
        id=result_id, user_id=current_user.id
    )
    if not result:
        raise HTTPException(status_code=422, detail="Результат не найден")
    return result


@router.get("", response_model=List[ResultWithTest])
async def get_results(
    current_user: Annotated[User, Depends(AccessController().get_access)],
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
):
    results = await uow.results.get_results_with_tests(user_id=current_user.id)
    return results
