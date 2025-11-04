from typing import Annotated, List

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.depends.uow import get_uow
from app.exceptions.exceptions import InvalidTokenError
from app.models.user import User
from app.repositories.unit_of_work import SQLAlchemyUnitOfWork
from app.services.auth import decode_access_token
from app.utils.types import Role

security = HTTPBearer(scheme_name="Authorization", auto_error=False, bearerFormat="JWT")


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
) -> User:
    try:
        if not credentials:
            raise InvalidTokenError
        decoded_token = decode_access_token(credentials.credentials)
        if not decoded_token:
            raise InvalidTokenError
        user = await uow.users.get(id=decoded_token["user_id"])
        if not user:
            raise InvalidTokenError
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Токен не валиден")


class AccessController:

    def __init__(
        self, required_roles: List[Role] = [Role.student, Role.teacher]
    ) -> None:
        required_roles.append(Role.admin)
        self.required_roles = required_roles

    async def get_access(
        self, access: Annotated[User, Depends(get_current_user)]
    ) -> User:
        if access.role not in self.required_roles:
            raise HTTPException(status_code=403, detail="Доступ запрещён")
        return access
