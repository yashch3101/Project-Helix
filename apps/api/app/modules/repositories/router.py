from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.repositories.schemas import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.modules.repositories.service import RepositoryService

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.post(
    "/import",
    response_model=RepositoryResponse,
)
async def import_repository(
    payload: RepositoryCreate,
    db: AsyncSession = Depends(get_db),
):
    return await RepositoryService.import_repository(
        db,
        payload,
    )