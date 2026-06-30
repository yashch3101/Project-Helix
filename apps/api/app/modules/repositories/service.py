from app.modules.repositories.git import GitService
from app.modules.repositories.github import get_repository_name
from app.modules.repositories.models import Repository
from app.modules.repositories.repository import RepositoryRepository


class RepositoryService:

    @staticmethod
    async def import_repository(
        db,
        payload,
    ):

        repository_name = get_repository_name(
            str(payload.github_url),
        )

        local_path = GitService.clone(
            str(payload.github_url),
            repository_name,
        )

        repository = Repository(
            name=repository_name,
            github_url=str(payload.github_url),
            local_path=local_path,
            project_id=payload.project_id,
            status="cloned",
        )

        return await RepositoryRepository.create(
            db,
            repository,
        )