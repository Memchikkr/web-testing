from datetime import UTC, datetime

from sqlmodel import Field, Relationship, SQLModel


class Enrollment(SQLModel, table=True):
    __tablename__ = "enrollment"
    
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    course_id: int = Field(foreign_key="course.id")
    enrolled_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = Field(default=None)
    progress_percent: float = Field(default=0.0)

    user: "User" = Relationship(back_populates="enrollments")  # type: ignore # noqa: F821
    course: "Course" = Relationship(back_populates="enrollments")  # type: ignore # noqa: F821
