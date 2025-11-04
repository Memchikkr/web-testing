from datetime import UTC, datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.question import Question


class Test(SQLModel, table=True):
    __tablename__ = "test"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    description: str = Field()
    creator_id: int = Field(foreign_key="user.id")
    time_limit_minutes: int = Field()
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    user: Optional["User"] = Relationship(back_populates="tests")  # type: ignore # noqa: F821
    questions: List[Question] = Relationship(back_populates="test")
    results: List["Result"] = Relationship(back_populates="test")  # type: ignore # noqa: F821
