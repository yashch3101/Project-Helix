from app.modules.retrieval.retrieval_pipeline import RetrievalPipeline
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


class RetrievalService:

    @staticmethod
    async def search(
        db: AsyncSession,
        repository_id: UUID,
        query: str,
        top_k: int = 10,
    ):

        results = await RetrievalPipeline.retrieve(

            db=db,

            repository_id=repository_id,

            query=query,

            top_k=top_k,

        )

        return results