from app.modules.repositories.git import GitService
from app.modules.repositories.github import get_repository_name
from app.modules.repositories.models import Repository
from app.modules.repositories.repository import RepositoryRepository
from app.modules.parser.file_scanner import FileScanner
from app.modules.repository_index.service import RepositoryIndexService


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

        # Scan repository
        scanned_files = FileScanner.scan(local_path)

        # Create repository object
        repository = Repository(
            name=repository_name,
            github_url=str(payload.github_url),
            local_path=local_path,
            project_id=payload.project_id,
            status="cloned",
        )

        # Save repository first
        repository = await RepositoryRepository.create(
            db,
            repository,
        )

        # Now repository.id exists
        await RepositoryIndexService.index_repository(
            db=db,
            repository=repository,
            scanned_files=scanned_files,
        )

        return repository