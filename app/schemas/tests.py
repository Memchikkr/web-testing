from datetime import datetime
from typing import List

from pydantic import ConfigDict, Field

from app.schemas import CustomBaseModel
from app.schemas.questions import QuestionBase, QuestionWithAnswer


class TestCreateRequest(CustomBaseModel):
    title: str = Field(min_length=5, max_length=64)
    description: str = Field(min_length=1, max_length=200)
    time_limit_minutes: int = Field(ge=1, le=10080)


class TestBase(CustomBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    creator_id: int
    time_limit_minutes: int
    created_at: datetime


class TestWithQuestions(TestBase):
    questions: List[QuestionBase]


class TestWithQuestionsAndAnswers(TestWithQuestions):
    questions: List[QuestionWithAnswer]
