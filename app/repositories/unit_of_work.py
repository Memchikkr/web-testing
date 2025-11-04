from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.repositories.answer import AnswerRepository
from app.repositories.question import QuestionRepository
from app.repositories.result import ResultRepository
from app.repositories.testing import TestRepository
from app.repositories.user import UserAnswerRepository, UserRepository


class IUnitOfWork(ABC):
    """Абстракция UOW для работы с транзакциями."""

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self._session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    @property
    def session(self) -> AsyncSession:
        if not hasattr(self, "_session"):
            raise RuntimeError("Сессия не инициализирована")
        return self._session

    @property
    def answers(self):
        if not hasattr(self, "_answers"):
            self._answers = AnswerRepository(self.session)
        return self._answers

    @property
    def questions(self):
        if not hasattr(self, "_questions"):
            self._questions = QuestionRepository(self.session)
        return self._questions

    @property
    def results(self):
        if not hasattr(self, "_results"):
            self._results = ResultRepository(self.session)
        return self._results

    @property
    def tests(self):
        if not hasattr(self, "_tests"):
            self._tests = TestRepository(self.session)
        return self._tests

    @property
    def users(self):
        if not hasattr(self, "_users"):
            self._users = UserRepository(self.session)
        return self._users

    @property
    def user_answers(self):
        if not hasattr(self, "_user_answers"):
            self._user_answers = UserAnswerRepository(self.session)
        return self._user_answers
