import traceback

from app.modules.parser.service import ParserService
from app.modules.code_chunks.service import CodeChunkService
from app.modules.embeddings.service import EmbeddingService
from app.modules.indexing.service import IndexingService

from app.modules.repositories.git import GitService
from app.modules.repositories.github import get_repository_name
from app.modules.repositories.models import Repository
from app.modules.repositories.repository import RepositoryRepository
from app.modules.parser.file_scanner import FileScanner
from app.modules.repository_index.service import RepositoryIndexService
from app.db.session import AsyncSessionLocal
from app.modules.graph.service import GraphService
from app.modules.knowledge_graph.service import (
    KnowledgeGraphService,
)
from app.modules.repository_summary.service import RepositorySummaryService


class RepositoryService:

    @staticmethod
    async def import_repository(
        db,
        payload,
        background_tasks,
    ):

        if "github.com" not in str(payload.github_url):

            raise ValueError(
                "Invalid GitHub repository URL."
            )

        repository_name = get_repository_name(
            str(payload.github_url),
        )

        # Create repository object
        repository = Repository(
            name=repository_name,
            github_url=str(payload.github_url),
            local_path="",
            project_id=payload.project_id,
            status="pending",
        )

        existing = await RepositoryRepository.get_by_project(
            db=db,
            project_id=payload.project_id,
        )

        for repo in existing:

            if repo.github_url == str(payload.github_url):

                raise ValueError(
                    "Repository already imported."
                )

        # Save repository first
        repository = await RepositoryRepository.create(
            db,
            repository,
        )

        print("ADDING BACKGROUND TASK")

        background_tasks.add_task(
            RepositoryService.process_repository,
            repository.id,
        )
        print("BACKGROUND TASK ADDED")

        return repository

    @staticmethod
    async def get_by_project(
        db,
        project_id,
    ):
        return await RepositoryRepository.get_by_project(
            db=db,
            project_id=project_id
        )

    @staticmethod
    async def get_status(
        db,
        repository_id,
    ):

        repository = await RepositoryRepository.get_by_id(
            db=db,
            repository_id=repository_id,
        )

        if repository is None:
            raise Exception("Repository not found")

        return repository

    @staticmethod
    async def sync(
        db,
        repository_id,
    ):

        repository = await RepositoryRepository.get_by_id(
            db=db,
            repository_id=repository_id,
        )

        if repository is None:
            raise Exception("Repository not found")

        await RepositoryRepository.update_progress(
            db=db,
            repository=repository,
            status="CLONING",
            progress=5,
            current_stage="Cloning repository...",
        )

        # Pull latest changes
        GitService.pull(
            repository.local_path,
        )

        # Scan repository
        scanned_files = FileScanner.scan(
            repository.local_path,
        )

        print("=" * 80)
        print("SCANNED FILES")

        for f in scanned_files:
            print(
                f["name"],
                f["extension"],
            )

        print("=" * 80)

        # Detect changes
        added, modified, deleted = (
            await RepositoryIndexService.detect_changed_files(
                db=db,
                repository=repository,
                scanned_files=scanned_files,
            )
        )

        # Remove deleted files
        await RepositoryIndexService.remove_deleted_files(
            db=db,
            deleted_files=deleted,
        )

        # Remove modified files
        await RepositoryIndexService.remove_modified_files(
            db=db,
            modified_files=modified,
        )

        # Index new files
        await RepositoryIndexService.index_files(
            db=db,
            repository=repository,
            scanned_files=added,
        )

        # Index modified files
        modified_files = (
            RepositoryIndexService.extract_scanned_files(
                modified
            )
        )

        await RepositoryIndexService.index_files(
            db=db,
            repository=repository,
            scanned_files=modified_files,
        )

        await RepositoryRepository.update_progress(
            db=db,
            repository=repository,
            status="READY",
            progress=100,
            current_stage="Repository ready.",
        )

        return repository

    @staticmethod
    async def process_repository(
        repository_id,
    ):
        try:

            print("=" * 50)
            print("PROCESS REPOSITORY STARTED")
            print(repository_id)
            print("=" * 50)

            async with AsyncSessionLocal() as db:

                print("=" * 80)
                print("BACKGROUND TASK STARTED")
                print(repository_id)

                repository = await RepositoryRepository.get_by_id(
                    db=db,
                    repository_id=repository_id,
                )

                if repository is None:
                    return

                repository = await RepositoryRepository.update_progress(
                    db=db,
                    repository=repository,
                    status="CLONING",
                    progress=5,
                    current_stage="Cloning repository...",
                )

                print("STATUS UPDATED")

                local_path = GitService.clone(
                    repository.github_url,
                    repository.name,
                )
                print("✅ STEP 1 : Clone Completed")

                print(local_path)

                repository = await RepositoryRepository.update_local_path(
                    db=db,
                    repository=repository,
                    local_path=local_path,
                )

                print("LOCAL PATH SAVED")

                await RepositoryRepository.update_progress(
                    db=db,
                    repository=repository,
                    status="PARSING",
                    progress=20,
                    current_stage="Scanning repository files...",
                )

                scanned_files = FileScanner.scan(
                    local_path,
                )

                await RepositoryIndexService.index_repository(
                    db=db,
                    repository=repository,
                    scanned_files=scanned_files,
                )
                print("✅ STEP 2 : Repository Indexed")

                print("=" * 80)
                print("REPOSITORY FILES INDEXED")
                print("=" * 80)

                print("🚀 STEP 3 : Starting Parser")
                await ParserService.parse_repository(
                    db=db,
                    repository_id=repository.id,
                )
                print("✅ STEP 4 : Parser Finished")

                await RepositoryRepository.update_progress(
                    db=db,
                    repository=repository,
                    status="GRAPH",
                    progress=40,
                    current_stage="Building knowledge graph...",
                )

                await KnowledgeGraphService.build(
                    db=db,
                )

                print("=" * 80)
                print("BUILDING GRAPH")
                print("=" * 80)

                await GraphService.build_graph(
                    db=db,
                    repository_id=repository.id,
                )

                print("=" * 80)
                print("GRAPH READY")
                print("=" * 80)

                # ===============================
                # Repository Knowledge Card
                # ===============================

                await RepositorySummaryService.test(
                    db=db,
                    repository_id=repository.id,
                )

                await RepositoryRepository.update_progress(
                    db=db,
                    repository=repository,
                    status="CHUNKING",
                    progress=55,
                    current_stage="Creating semantic chunks...",
                )

                print("=" * 80)
                print("SUMMARY GENERATED")
                print("=" * 80)

                await CodeChunkService.build_chunks(
                    db=db,
                    repository_id=repository.id,
                )

                await RepositoryRepository.update_progress(
                    db=db,
                    repository=repository,
                    status="GRAPH",
                    progress=65,
                    current_stage="Building knowledge graph...",
                )

                print("=" * 80)
                print("PARSER COMPLETED")
                print("=" * 80)

                await RepositoryRepository.update_progress(
                    db=db,
                    repository=repository,
                    status="EMBEDDING",
                    progress=80,
                    current_stage="Generating embeddings...",
                )

                await EmbeddingService.generate(
                    db=db,
                )

                print("=" * 80)
                print("EMBEDDINGS GENERATED")
                print("=" * 80)

                await RepositoryRepository.update_progress(
                    db=db,
                    repository=repository,
                    status="INDEXING",
                    progress=95,
                    current_stage="Building hybrid search index...",
                )

                await IndexingService.rebuild(
                    db=db,
                    repository_id=repository.id,
                )

                print("=" * 80)
                print("BM25 REBUILT")
                print("=" * 80)

                await RepositoryRepository.update_progress(
                    db=db,
                    repository=repository,
                    status="READY",
                    progress=100,
                    current_stage="Repository ready.",
                )

                print("=" * 80)
                print("FULL PIPELINE COMPLETED")
                print("=" * 80)

        except Exception as e:

            print("=" * 80)
            print("BACKGROUND ERROR")
            traceback.print_exc()
            print("=" * 80)

            try:

                async with AsyncSessionLocal() as db:

                    repository = await RepositoryRepository.get_by_id(
                        db=db,
                        repository_id=repository_id,
                    )

                    if repository:

                        await RepositoryRepository.update_progress(
                            db=db,
                            repository=repository,
                            status="FAILED",
                            progress=100,
                            current_stage="Repository processing failed.",
                        )

                        repository.error_message = str(e)

                        await db.commit()

            except Exception:

                traceback.print_exc()