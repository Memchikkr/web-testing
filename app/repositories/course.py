from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from app.repositories.repository import SQLAlchemyRepository


class CourseRepository(SQLAlchemyRepository[Course]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Course)
