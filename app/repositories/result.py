from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.models.question import Question
from app.models.result import Result
from app.models.testing import Test
from app.repositories.repository import SQLAlchemyRepository


class ResultRepository(SQLAlchemyRepository[Result]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Result)

    async def get_result_with_test_and_answers(self, **filter_by) -> Result | None:
        stmt = (
            select(self._model)
            .options(
                joinedload(self._model.test).options(
                    joinedload(Test.questions).options(joinedload(Question.answer))
                ),
                joinedload(self._model.answers),
            )
            .filter_by(**filter_by)
        )
        result = await self._session.execute(stmt)
        result = result.unique().scalar_one_or_none()
        return result

    async def get_results_with_tests(self, **filter_by) -> List[Result]:
        stmt = (
            select(self._model)
            .options(joinedload(self._model.test))
            .filter_by(**filter_by)
        )
        result = await self._session.execute(stmt)
        result = result.scalars().all()
        return result
