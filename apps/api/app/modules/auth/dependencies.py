from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.modules.auth.repository import AuthRepository

from app.core.config import settings

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    try:

        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        user = await AuthRepository.get_by_id(
            db,
            payload["sub"],
        )

        if not user:

            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        return user

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )