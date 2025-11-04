from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enrollment import Enrollment
from app.repositories.repository import SQLAlchemyRepository


class EnrollmentRepository(SQLAlchemyRepository[Enrollment]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Enrollment)
