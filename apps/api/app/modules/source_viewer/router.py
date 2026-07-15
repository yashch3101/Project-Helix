from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.source_viewer.service import (
    SourceViewerService,
)

router = APIRouter(
    prefix="/source",
    tags=["Source"],
)


@router.get("/{symbol_id}")

async def get_source(
    symbol_id: str,
    db: AsyncSession = Depends(get_db),
):

    return await SourceViewerService.get_source(
        db,
        symbol_id,
    )