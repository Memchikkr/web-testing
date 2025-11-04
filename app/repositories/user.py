from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserAnswer
from app.repositories.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)


class UserAnswerRepository(SQLAlchemyRepository[UserAnswer]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserAnswer)
