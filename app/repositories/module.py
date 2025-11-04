from sqlalchemy.ext.asyncio import AsyncSession

from app.models.module import Module
from app.repositories.repository import SQLAlchemyRepository


class ModuleRepository(SQLAlchemyRepository[Module]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Module)
