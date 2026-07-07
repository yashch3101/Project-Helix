import hashlib
from pathlib import Path

from app.modules.repository_index.models import RepositoryFile
from app.modules.repository_index.repository import (
    RepositoryIndexRepository,
)


class RepositoryIndexService:

    @staticmethod
    async def index_repository(
        db,
        repository,
        scanned_files,
    ):

        database_files = []

        for file in scanned_files:

            sha = hashlib.sha256(
                Path(file["absolute_path"]).read_bytes()
            ).hexdigest()

            repository_file = RepositoryFile(
                repository_id=repository.id,
                file_name=file["name"],
                relative_path=file["relative_path"],
                absolute_path=file["absolute_path"],
                extension=file["extension"],
                language=file["language"],
                size=file["size"],
                sha256=sha,
                modified_time="",
            )

            database_files.append(
                repository_file
            )

        await RepositoryIndexRepository.bulk_insert(
            db,
            database_files,
        )