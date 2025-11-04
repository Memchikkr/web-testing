from pydantic import ConfigDict, Field

from app.schemas import CustomBaseModel
from app.schemas.answers import AnswerBase
from app.utils.types import QuestionType


class QuestionCreateRequest(CustomBaseModel):
    question_text: str = Field(min_length=1, max_length=300)
    question_type: QuestionType = Field()
    points: int = Field(ge=1, le=10)


class QuestionBase(CustomBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    test_id: int
    question_text: str
    question_type: QuestionType
    points: int


class QuestionWithAnswer(CustomBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    test_id: int
    question_text: str
    question_type: QuestionType
    points: int
    answer: AnswerBase | None
