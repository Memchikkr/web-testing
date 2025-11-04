from datetime import UTC, datetime
from typing import List, Optional

from sqlmodel import Column, Enum, Field, LargeBinary, Relationship, SQLModel

from app.utils.types import Role


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password_hash: bytes = Field(sa_column=Column(LargeBinary(32)))
    password_salt: bytes = Field(sa_column=Column(LargeBinary(16)))
    access_token: str | None = Field(default=None)
    role: str = Field(sa_column=Column(Enum(Role)))
    first_name: str = Field()
    last_name: str = Field()
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    tests: List["Test"] = Relationship(back_populates="user")  # type: ignore # noqa: F821
    results: List["Result"] = Relationship(back_populates="user")  # type: ignore # noqa: F821
    enrollments: List["Enrollment"] = Relationship(back_populates="user")  # type: ignore # noqa: F821
    courses: List["Course"] = Relationship(back_populates="user")  # type: ignore # noqa: F821


class UserAnswer(SQLModel, table=True):
    __tablename__ = "user_answer"

    result_id: int = Field(foreign_key="result.id", primary_key=True)
    question_id: int = Field(foreign_key="question.id", primary_key=True)
    answer_id: int = Field(foreign_key="answer.id", primary_key=True)
    answer_text: str = Field()
    is_correct: bool = Field()

    result: Optional["Result"] = Relationship(back_populates="answers")  # type: ignore # noqa: F821
    question: Optional["Question"] = Relationship()  # type: ignore # noqa: F821
    answer: Optional["Answer"] = Relationship()  # type: ignore # noqa: F821
