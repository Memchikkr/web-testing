from datetime import datetime

from pydantic import ConfigDict

from app.schemas import CustomBaseModel
from app.utils.types import Role


class UserBase(CustomBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: Role
    first_name: str
    last_name: str
    created_at: datetime


class UserAnswerRequest(CustomBaseModel):
    question_id: int
    answer_text: str


class UserAnswerShort(CustomBaseModel):
    model_config = ConfigDict(from_attributes=True)

    result_id: int
    question_id: int
    answer_id: int
    answer_text: str


class UserAnswerBase(UserAnswerShort):
    is_correct: bool | None
