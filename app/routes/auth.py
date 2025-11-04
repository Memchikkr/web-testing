from fastapi import APIRouter, Depends, HTTPException

from app.models.user import User
from app.repositories import get_uow
from app.repositories.unit_of_work import SQLAlchemyUnitOfWork
from app.repositories.user import UserRepository
from app.schemas.auth import AuthRequest, AuthResponse, RegistrationRequest
from app.services.auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="", tags=["Authentification"])


@router.post("/registration", response_model=AuthResponse)
async def registration(
    request: RegistrationRequest, uow: SQLAlchemyUnitOfWork = Depends(get_uow)
):
    rep = UserRepository(session=uow.session)
    result = await rep.get(email=request.email)
    if result:
        raise HTTPException(status_code=403, detail="Email уже занят")

    hash, salt = hash_password(request.password)
    user = User(
        username=request.username,
        email=request.email,
        password_hash=hash,
        password_salt=salt,
        role=request.role,
        first_name=request.first_name,
        last_name=request.last_name,
    )
    rep.add(user)
    token, secret = create_access_token({"user_id": user.id})
    await rep.update({"access_token": secret}, id=user.id)
    await uow.commit()
    return AuthResponse(access_token=token)


@router.post("/login", response_model=AuthResponse)
async def login(request: AuthRequest, uow: SQLAlchemyUnitOfWork = Depends(get_uow)):
    rep = UserRepository(session=uow.session)
    user: User | None = await rep.get(email=request.email)

    if not user:
        raise HTTPException(status_code=401, detail="Неверный email")
    if not verify_password(request.password, user.password_hash, user.password_salt):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    access_token, secret = create_access_token(payload={"user_id": user.id})
    await rep.update({"access_token": secret}, id=user.id)
    await uow.commit()
    return AuthResponse(access_token=access_token)
