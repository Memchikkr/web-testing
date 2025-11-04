from datetime import UTC, datetime
from typing import List

from sqlmodel import Field, Relationship, SQLModel

from app.utils.types import CourseStatus


class Course(SQLModel, table=True):
    __tablename__ = "course"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    status: CourseStatus = Field(default=CourseStatus.DRAFT)
    image_url: str | None = Field(default=None)
    price: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    modules: List["Module"] = Relationship(back_populates="course")  # type: ignore # noqa: F821
    enrollments: List["Enrollment"] = Relationship(back_populates="course")  # type: ignore # noqa: F821
    user: "User" = Relationship(back_populates="courses")  # type: ignore # noqa: F821
