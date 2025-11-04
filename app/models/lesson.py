from sqlalchemy import Text
from sqlmodel import Field, Relationship, SQLModel


class Lesson(SQLModel, table=True):
    __tablename__ = "lesson"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    content: str = Field(sa_type=Text)
    order_index: int = Field(default=1)
    module_id: int = Field(foreign_key="module.id")

    module: "Module" = Relationship(back_populates="lessons")  # type: ignore # noqa: F821
