from collections.abc import AsyncIterator
from app.database.session import async_session_maker

from app.repositories.unit_of_work import SQLAlchemyUnitOfWork


async def get_uow() -> AsyncIterator[SQLAlchemyUnitOfWork]:
    uow = SQLAlchemyUnitOfWork(async_session_maker)
    async with uow:
        yield uow
