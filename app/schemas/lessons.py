from pydantic import Field

from app.schemas import CustomBaseModel


class LessonCreate(CustomBaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    order_index: int = Field(default=1, ge=1)


class LessonUpdate(CustomBaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    order_index: int | None = Field(default=None, ge=1)


class LessonRead(CustomBaseModel):
    id: int
    title: str
    content: str
    order_index: int
    module_id: int
