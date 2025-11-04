from datetime import datetime
from typing import List

from pydantic import Field

from app.schemas import CustomBaseModel
from app.schemas.modules import ModuleRead
from app.utils.types import CourseStatus


class CourseCreate(CustomBaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=1000)
    status: CourseStatus = Field(default=CourseStatus.DRAFT)
    image_url: str | None = Field(default=None, min_length=1)


class CourseUpdate(CustomBaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    status: CourseStatus | None = Field(default=None)
    image_url: str | None = Field(default=None, min_length=1)


class CourseRead(CustomBaseModel):
    id: int
    title: str
    description: str
    status: CourseStatus
    image_url: str | None
    created_at: datetime
    updated_at: datetime


class CourseDetail(CourseRead):
    modules: List[ModuleRead]
