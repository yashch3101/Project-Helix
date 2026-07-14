from sqlalchemy import select

from app.modules.code_chunks.models import CodeChunk
from app.modules.dependency_graph.models import CodeDependency
from app.modules.repository_index.models import RepositoryFile


class DependencyExpansionRepository:

    @staticmethod
    async def get_dependencies(
        db,
        repository_id,
        symbol_name,
    ):

        result = await db.execute(

            select(CodeDependency)

            .join(

                RepositoryFile,

                RepositoryFile.id == CodeDependency.source_file_id,
            )

            .where(

                RepositoryFile.repository_id == repository_id
            )

            .where(

                CodeDependency.target_name == symbol_name
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_chunks_by_file(

        db,

        repository_file_id,
    ):

        result = await db.execute(

            select(CodeChunk)

            .where(

                CodeChunk.repository_file_id == repository_file_id
            )

            .order_by(

                CodeChunk.start_line
            )
        )

        return result.scalars().all()