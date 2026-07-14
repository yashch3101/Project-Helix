from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.retrieval.vector_search import VectorSearch
from app.modules.retrieval.hybrid_search import HybridSearch


class RetrievalPipeline:

    @staticmethod
    async def retrieve(
        db: AsyncSession,
        repository_id,
        query: str,
        top_k: int,
    ):

        results = await HybridSearch.search(

            db=db,

            repository_id=repository_id,

            query=query,

            top_k=top_k,

        )

        return results[:top_k]