from sqlalchemy.ext.asyncio import AsyncSession

from app.models.answer import Answer
from app.repositories.repository import SQLAlchemyRepository


class AnswerRepository(SQLAlchemyRepository[Answer]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Answer)
