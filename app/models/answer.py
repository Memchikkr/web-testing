from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Answer(SQLModel, table=True):
    __tablename__ = "answer"

    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id")
    answer_text: str = Field()

    question: Optional["Question"] = Relationship(back_populates="answer")  # type: ignore # noqa: F821
