from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.scanner.schemas import (
    RepositoryFileResponse,
    ScanRepositoryRequest,
)
from app.modules.scanner.service import ScannerService

router = APIRouter(
    prefix="/scanner",
    tags=["Scanner"],
)


@router.post(
    "/scan",
    response_model=list[RepositoryFileResponse],
)
async def scan_repository(
    payload: ScanRepositoryRequest,
    db: AsyncSession = Depends(get_db),
):

    return await ScannerService.scan_repository(
        db,
        payload.repository_id,
    )