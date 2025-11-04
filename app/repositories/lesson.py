from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson import Lesson
from app.repositories.repository import SQLAlchemyRepository


class LessonRepository(SQLAlchemyRepository[Lesson]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Lesson)
