from datetime import datetime
from typing import List

from pydantic import ConfigDict, model_validator

from app.schemas import CustomBaseModel
from app.schemas.tests import TestBase, TestWithQuestionsAndAnswers
from app.schemas.users import UserAnswerBase


class ResultBase(CustomBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    test_id: int
    score: int | None
    started_at: datetime
    finished_at: datetime | None

    @model_validator(mode="after")
    def validate_model(self):
        if self.finished_at is None:
            self.score = None
        return self

class ResultWithTest(ResultBase):
    test: TestBase


class ResultWithTestAndAnswers(ResultBase):
    test: TestWithQuestionsAndAnswers
    answers: List[UserAnswerBase]

    @model_validator(mode="after")
    def validate_model(self):
        if self.finished_at is None:
            self.score = None
            for answer in self.answers:
                answer.is_correct = False
        for i, question in enumerate(self.test.questions):
            if question.answer is None:
                self.test.questions.remove(question)
            if self.finished_at is None:
                self.test.questions[i].answer = None
        return self
