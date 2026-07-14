import asyncio

from app.db.session import AsyncSessionLocal
from app.modules.repositories.repository import RepositoryRepository
from app.modules.parser.file_scanner import FileScanner
from app.modules.repository_index.service import RepositoryIndexService


REPOSITORY_ID = "7e8360ee-1bd9-4bf3-b7f0-df42ca3c063c"


async def main():

    async with AsyncSessionLocal() as db:

        repository = await RepositoryRepository.get_by_id(
            db=db,
            repository_id=REPOSITORY_ID,
        )

        scanned_files = FileScanner.scan(
            repository.local_path
        )

        await RepositoryIndexService.detect_changed_files(
            db=db,
            repository=repository,
            scanned_files=scanned_files,
        )


asyncio.run(main())