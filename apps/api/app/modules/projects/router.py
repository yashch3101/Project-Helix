from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.projects.schemas import (
    ProjectCreate,
    ProjectResponse,
)
from app.modules.projects.service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
)
async def create_project(
    payload: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await ProjectService.create(
        db,
        payload,
        current_user["sub"],
    )


@router.get(
    "",
    response_model=list[ProjectResponse],
)
async def get_projects(
    db: AsyncSession = Depends(get_db),
):
    return await ProjectService.get_all(db)