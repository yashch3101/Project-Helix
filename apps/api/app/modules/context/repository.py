from sqlalchemy import select

from app.modules.code_chunks.models import CodeChunk

from app.modules.retrieval.repository import RetrievalRepository


class ContextRepository:

    @staticmethod
    async def retrieve(
        db,
        repository_id,
        query_vector,
        top_k,
    ):
        return await RetrievalRepository.semantic_search(
            db=db,
            repository_id=repository_id,
            query_vector=query_vector,
            top_k=top_k,
        )

    @staticmethod
    async def get_neighbour_chunks(
        db,
        repository_file_id,
        start_line,
        window=40,
    ):

        result = await db.execute(

            select(CodeChunk)

            .where(
                CodeChunk.repository_file_id == repository_file_id
            )

            .where(
                CodeChunk.start_line >= start_line - window
            )

            .where(
                CodeChunk.start_line <= start_line + window
            )

            .order_by(CodeChunk.start_line)

        )

        return result.scalars().all()

    @staticmethod
    async def get_chunk(
        db,
        chunk_id,
    ):

        result = await db.execute(

            select(CodeChunk).where(

                CodeChunk.id == chunk_id

            )

        )

        return result.scalar_one_or_none()