from pydantic import ConfigDict, Field

from app.schemas import CustomBaseModel


class AnswerCreateRequest(CustomBaseModel):
    answer_text: str = Field(min_length=1, max_length=100)


class AnswerBase(CustomBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    answer_text: str
