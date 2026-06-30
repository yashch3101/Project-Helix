from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.schemas import UserCreate, UserResponse
from app.modules.auth.service import AuthService

from app.modules.auth.schemas import (
    UserLogin,
    TokenResponse,
)

from app.modules.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await AuthService.register(db, payload)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    payload: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await AuthService.login(
            db,
            payload.email,
            payload.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )

@router.get("/me")
async def me(
    current_user=Depends(get_current_user),
):
    return current_user