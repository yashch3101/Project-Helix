from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.modules.auth.models import User
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import UserCreate

from app.modules.auth.security import (
    verify_password,
    create_access_token,
)


class AuthService:

    @staticmethod
    async def register(
        db: AsyncSession,
        payload: UserCreate,
    ):
        existing = await AuthRepository.get_by_email(
            db,
            payload.email,
        )

        if existing:
            raise ValueError("Email already exists")

        user = User(
            full_name=payload.full_name,
            email=payload.email,
            hashed_password=hash_password(
                payload.password
            ),
        )

        return await AuthRepository.create_user(
            db,
            user,
        )

    @staticmethod
    async def login(
        db: AsyncSession,
        email: str,
        password: str,
    ):
        user = await AuthRepository.get_by_email(db, email)

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }