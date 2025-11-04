from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update

T = TypeVar("T")


class IRepository(Generic[T], ABC):
    """Абстракция репозитория для работы с сущностями."""

    @abstractmethod
    async def add(self, model: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, **filter_by) -> T | None:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, values: dict, **filter_by) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_conditions(self, **filter_by) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, model: T) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(IRepository[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self._session = session
        self._model = model

    def add(self, model: T) -> None:
        self._session.add(model)

    async def get(self, **filter_by) -> T | None:
        stmt = select(self._model).filter_by(**filter_by)
        result = await self._session.execute(stmt)
        result = result.scalar_one_or_none()
        return result

    async def update(self, values: dict, **filter_by) -> None:
        query = update(self._model).values(**values).filter_by(**filter_by)
        await self._session.execute(query)

    async def get_all_by_conditions(self, **filter_by) -> List[T]:
        query = select(self._model).filter_by(**filter_by)
        result = await self._session.execute(query)
        result = result.scalars().all()
        return result

    async def get_all(self) -> List[T]:
        query = select(self._model)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def delete_one(self, model: T) -> None:
        await self._session.delete(model)
