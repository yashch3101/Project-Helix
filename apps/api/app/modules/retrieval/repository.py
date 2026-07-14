from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.embeddings.models import CodeEmbedding
from app.modules.code_chunks.models import CodeChunk
from app.modules.repository_index.models import RepositoryFile


class RetrievalRepository:

    @staticmethod
    async def get_chunks_by_repository(
        db: AsyncSession,
        repository_id,
    ):

        result = await db.execute(
            select(
                CodeChunk,
                CodeEmbedding,
            )
            .join(
                CodeEmbedding,
                CodeChunk.id == CodeEmbedding.chunk_id,
            )
            .join(
                RepositoryFile,
                RepositoryFile.id == CodeChunk.repository_file_id,
            )
            .where(
                RepositoryFile.repository_id == repository_id
            )
        )

        return result.all()

    @staticmethod
    async def semantic_search(
        db: AsyncSession,
        repository_id,
        query_vector,
        top_k: int = 10,
    ):

        print("=" * 80)
        print("REPOSITORY ID:", repository_id)
        print("TYPE:", type(repository_id))
        print("=" * 80)

        sql = text("""
        SELECT

            c.id,
            c.repository_file_id,
            c.chunk_name,
            c.chunk_type,
            c.start_line,
            c.end_line,
            c.content,

            1 - (e.embedding <=> CAST(:embedding AS vector)) AS score

        FROM code_embeddings e

        JOIN code_chunks c
            ON c.id = e.chunk_id

        JOIN repository_files f
            ON f.id = c.repository_file_id

        WHERE f.repository_id = :repository_id

        ORDER BY e.embedding <=> CAST(:embedding AS vector)

        LIMIT :top_k
        """)

        params = {
            "repository_id": str(repository_id),
            "embedding": query_vector,
            "top_k": top_k,
        }

        print("=" * 80)
        print("SQL PARAMS")
        print(params)
        print("=" * 80)

        result = await db.execute(
            sql,
            params,
        )

        return result.mappings().all()

    @staticmethod
    async def load_all_chunks(
        db: AsyncSession,
        repository_id,
    ):

        result = await db.execute(
            select(CodeChunk)
            .join(
                RepositoryFile,
                RepositoryFile.id == CodeChunk.repository_file_id,
            )
            .where(
                RepositoryFile.repository_id == repository_id
            )
            .order_by(
                CodeChunk.start_line.asc()
            )
        )

        return result.scalars().all()