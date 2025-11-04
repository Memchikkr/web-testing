from datetime import datetime

from pydantic import Field

from app.schemas import CustomBaseModel


class EnrollmentCreate(CustomBaseModel):
    course_id: int = Field(ge=1)


class EnrollmentRead(CustomBaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    completed_at: datetime | None
    progress_percent: float
