from typing import List

from pydantic import Field

from app.schemas import CustomBaseModel
from app.schemas.lessons import LessonRead


class ModuleCreate(CustomBaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=500)
    order_index: int = Field(default=1, ge=1)


class ModuleUpdate(CustomBaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=500)
    order_index: int | None = Field(default=None, ge=1)


class ModuleRead(CustomBaseModel):
    id: int
    title: str
    description: str | None
    order_index: int
    course_id: int
    lessons: List[LessonRead]
