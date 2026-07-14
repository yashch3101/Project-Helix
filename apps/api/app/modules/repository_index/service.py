import hashlib
from pathlib import Path

from app.modules.repository_index.models import RepositoryFile, RepositoryChunk
from app.modules.repository_index.repository import (
    RepositoryIndexRepository,
)

from app.modules.parser.chunker import chunk_file

class RepositoryIndexService:

    @staticmethod
    async def index_repository(
        db,
        repository,
        scanned_files,
    ):

        if not scanned_files:
            return

        await RepositoryIndexService.index_files(
            db=db,
            repository=repository,
            scanned_files=scanned_files,
        )

    @staticmethod
    async def detect_changed_files(
        db,
        repository,
        scanned_files,
    ):
        database_files = await RepositoryIndexRepository.get_files(
        db=db,
        repository_id=repository.id,
    )

        database_map = {
        file.relative_path: file
        for file in database_files
    }

        scan_map = {
            file["relative_path"]: file
            for file in scanned_files
        }

        added = []

        modified = []

        deleted = []

        for relative_path, scanned in scan_map.items():

            if relative_path not in database_map:

                added.append(scanned)

                continue

            db_file = database_map[relative_path]

            current_sha = hashlib.sha256(
                Path(
                    scanned["absolute_path"]
                ).read_bytes()
            ).hexdigest()

            if current_sha != db_file.sha256:

                modified.append(
                    (
                        db_file,
                        scanned,
                    )
                )

        for relative_path, db_file in database_map.items():

            if relative_path not in scan_map:

                deleted.append(db_file)

        print("=" * 80)
        print("Added:", len(added))
        print("Modified:", len(modified))
        print("Deleted:", len(deleted))
        print("=" * 80)

        return added, modified, deleted

    @staticmethod
    async def remove_deleted_files(
        db,
        deleted_files,
    ):

        for repository_file in deleted_files:

            await RepositoryIndexRepository.delete_file(
                db=db,
                repository_file=repository_file,
            )

        print("=" * 80)
        print(f"Deleted Files: {len(deleted_files)}")
        print("=" * 80)

    @staticmethod
    async def index_files(
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

        database_chunks = []

        for repository_file in database_files:

            chunks = chunk_file(
                repository_file.absolute_path
            )

            for index, chunk in enumerate(chunks):

                database_chunks.append(

                    RepositoryChunk(

                        repository_file_id=repository_file.id,

                        chunk_index=index,

                        start_line=chunk["start_line"],

                        end_line=chunk["end_line"],

                        content=chunk["content"],

                    )

                )

        print("=" * 80)
        print("FILES:", len(database_files))
        print("CHUNKS:", len(database_chunks))
        print("=" * 80)

        await RepositoryIndexRepository.bulk_insert(
            db,
            database_chunks,
        )

    @staticmethod
    async def remove_modified_files(
        db,
        modified_files,
    ):

        for repository_file, _ in modified_files:

            await RepositoryIndexRepository.delete_file(
                db=db,
                repository_file=repository_file,
            )

        print("=" * 80)
        print(f"Modified Files Removed: {len(modified_files)}")
        print("=" * 80)

    @staticmethod
    def extract_scanned_files(
        modified_files,
    ):

        return [

            scanned_file

            for _, scanned_file

            in modified_files

        ]