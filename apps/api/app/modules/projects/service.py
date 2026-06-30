from app.modules.projects.models import Project
from app.modules.projects.repository import ProjectRepository


class ProjectService:

    @staticmethod
    async def create(
        db,
        payload,
        owner_id
    ):
        project = Project(
            name=payload.name,
            description=payload.description,
            owner_id=owner_id,
        )

        return await ProjectRepository.create(
            db,
            project,
        )

    @staticmethod
    async def get_all(
        db,
    ):
        return await ProjectRepository.get_all(db)