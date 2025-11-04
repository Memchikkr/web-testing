from typing import Annotated

from fastapi import APIRouter, Depends

from app.bearer import AccessController
from app.models.user import User
from app.schemas.users import UserBase

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(AccessController().get_access)],
)


@router.get("/me", response_model=UserBase)
async def get_me(
    current_user: Annotated[User, Depends(AccessController().get_access)],
):
    return current_user
