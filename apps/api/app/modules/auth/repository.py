from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User


class AuthRepository:

    @staticmethod
    async def get_by_email(
        db: AsyncSession,
        email: str,
    ):
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        db: AsyncSession,
        user: User,
    ):
        db.add(user)
        print("ADD DONE")
        await db.commit()
        print("COMMIT DONE")
        await db.refresh(user)
        print("REFRESH DONE")
        return user

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        user_id: str,
    ):
        result = await db.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()