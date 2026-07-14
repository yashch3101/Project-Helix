from uuid import UUID
from fastapi import APIRouter, Depends, BackgroundTasks
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
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    return await RepositoryService.import_repository(
        db=db,
        payload=payload,
        background_tasks=background_tasks,
    )

@router.get(
    "/project/{project_id}",
)
async def get_project_repositories(
    project_id: str,
    db: AsyncSession = Depends(get_db),
):

    repositories = await RepositoryService.get_by_project(
        db=db,
        project_id=project_id,
    )

    return [
        {
            "id": str(repo.id),
            "name": repo.name,
            "status": repo.status,
            "github_url": repo.github_url,
        }
        for repo in repositories
    ]

@router.post(
    "/{repository_id}/sync"
)
async def sync_repository(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    return await RepositoryService.sync(
        db=db,
        repository_id=repository_id,
    )