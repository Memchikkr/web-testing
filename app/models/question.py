from typing import Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from app.utils.types import QuestionType


class Question(SQLModel, table=True):
    __tablename__ = "question"

    id: int | None = Field(default=None, primary_key=True)
    test_id: int = Field(foreign_key="test.id")
    question_text: str = Field()
    question_type: str = Field(sa_column=Column(Enum(QuestionType)))
    points: int = Field()

    test: Optional["Test"] = Relationship(back_populates="questions")  # type: ignore # noqa: F821
    answer: Optional["Answer"] = Relationship(back_populates="question")  # type: ignore # noqa: F821
