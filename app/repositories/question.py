from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question import Question
from app.repositories.repository import SQLAlchemyRepository


class QuestionRepository(SQLAlchemyRepository[Question]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Question)
