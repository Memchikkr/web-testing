from typing import List

from sqlmodel import Field, Relationship, SQLModel


class Module(SQLModel, table=True):
    __tablename__ = "module"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=500)
    order_index: int = Field(default=1)
    course_id: int = Field(foreign_key="course.id")

    course: "Course" = Relationship(back_populates="modules")  # type: ignore # noqa: F821
    lessons: List["Lesson"] = Relationship(back_populates="module")  # type: ignore # noqa: F821
