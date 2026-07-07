from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.embeddings.embedder import Embedder
from app.modules.retrieval.repository import RetrievalRepository


class RetrievalService:

    @staticmethod
    async def search(
        db: AsyncSession,
        repository_id,
        query: str,
        top_k: int = 10,
    ):

        # Encode query
        query_vector = Embedder.encode(query)

        # Convert list -> pgvector string
        query_vector = "[" + ",".join(map(str, query_vector)) + "]"

        # PostgreSQL + pgvector search
        results = await RetrievalRepository.semantic_search(
            db=db,
            repository_id=repository_id,
            query_vector=query_vector,
            top_k=top_k,
        )

        return [
            {
                "score": float(row["score"]),
                "chunk_id": str(row["id"]),
                "chunk_name": row["chunk_name"],
                "chunk_type": row["chunk_type"],
                "start_line": row["start_line"],
                "end_line": row["end_line"],
                "content": row["content"],
            }
            for row in results
        ]