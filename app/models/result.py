from datetime import UTC, datetime
from typing import List, Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel


class Result(SQLModel, table=True):
    __tablename__ = "result"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    test_id: int = Field(foreign_key="test.id")
    score: int | None = Field(default=None)
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    finished_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )

    user: Optional["User"] = Relationship(back_populates="results")  # type: ignore # noqa: F821
    test: Optional["Test"] = Relationship(back_populates="results")  # type: ignore # noqa: F821
    answers: List["UserAnswer"] = Relationship(back_populates="result")  # type: ignore # noqa: F821
