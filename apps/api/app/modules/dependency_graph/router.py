from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.dependency_graph.service import DependencyService

router = APIRouter(
    prefix="/dependency-graph",
    tags=["Dependency Graph"],
)


@router.post("/{repository_id}")
async def build_dependency_graph(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await DependencyService.build(
        db,
        repository_id,
    )