from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, with_loader_criteria
from sqlmodel import select

from app.models.answer import Answer
from app.models.question import Question
from app.models.testing import Test
from app.repositories.repository import SQLAlchemyRepository


class TestRepository(SQLAlchemyRepository[Test]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Test)

    async def get_test_with_questions_and_answers(self, **filter_by) -> Test | None:
        stmt = (
            select(self._model)
            .options(
                joinedload(self._model.questions).options(joinedload(Question.answer)),
                with_loader_criteria(Answer, Answer.question_id == Question.id),
            )
            .filter_by(**filter_by)
        )
        result = await self._session.execute(stmt)
        result = result.unique().scalar_one_or_none()
        return result

    async def get_test_with_questions(self, **filter_by) -> Test | None:
        stmt = (
            select(self._model)
            .options(joinedload(self._model.questions))
            .filter_by(**filter_by)
        )
        result = await self._session.execute(stmt)
        result = result.unique().scalar_one_or_none()
        return result

    async def search_tests(self, filter: str | None) -> List[Test]:
        stmt = select(self._model)
        if filter:
            stmt = stmt.filter(self._model.title.like(f"%{filter}%"))
        result = await self._session.execute(stmt)
        result = result.unique().scalars().all()
        return result
