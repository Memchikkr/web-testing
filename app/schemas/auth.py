from pydantic import EmailStr, Field, ValidationError, field_validator

from app.schemas import CustomBaseModel
from app.utils.types import Role


class RegistrationRequest(CustomBaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr = Field()
    password: str = Field(min_length=5, max_length=32)
    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)
    role: Role

    @field_validator("role")
    def validate_role(cls, role):
        if role == Role.admin:
            raise ValidationError("Роль администратора запрещена для ввода")
        return role


class AuthRequest(CustomBaseModel):
    email: EmailStr = Field()
    password: str = Field(min_length=5, max_length=32)


class AuthResponse(CustomBaseModel):
    access_token: str
