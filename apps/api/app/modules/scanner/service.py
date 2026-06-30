import os

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.repositories.repository import RepositoryRepository
from app.modules.scanner.detector import detect_language
from app.modules.scanner.models import RepositoryFile
from app.modules.scanner.parser import collect_files
from app.modules.scanner.repository import ScannerRepository


class ScannerService:

    @staticmethod
    async def scan_repository(
        db: AsyncSession,
        repository_id,
    ):

        repository = await RepositoryRepository.get_by_id(
            db,
            repository_id,
        )

        if repository is None:
            raise Exception("Repository not found")

        files = collect_files(repository.local_path)

        scanned = []

        for file_path in files:

            filename = os.path.basename(file_path)

            extension = os.path.splitext(filename)[1]

            language = detect_language(extension)

            size = os.path.getsize(file_path)

            repository_file = RepositoryFile(
                repository_id=repository.id,
                path=file_path,
                filename=filename,
                extension=extension,
                language=language,
                size=size,
            )

            repository_file = await ScannerRepository.save(
                db,
                repository_file,
            )

            scanned.append(repository_file)

        return scanned