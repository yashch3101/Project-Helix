from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.embeddings.embedder import Embedder
from app.modules.retrieval.repository import RetrievalRepository
from app.modules.retrieval.types import RetrievalResult
from app.modules.retrieval.base import RetrievalStrategy


class VectorSearch(RetrievalStrategy):

    @staticmethod
    async def search(
        db: AsyncSession,
        repository_id,
        query: str,
        top_k: int,
    ):

        query_vector = Embedder.encode(query)

        query_vector = "[" + ",".join(
            map(str, query_vector)
        ) + "]"

        rows = await RetrievalRepository.semantic_search(
            db=db,
            repository_id=repository_id,
            query_vector=query_vector,
            top_k=top_k,
        )

        print("=" * 80)
        print("VECTOR SEARCH")
        print("Repository:", repository_id)
        print("Rows:", len(rows))

        for row in rows[:5]:
            print(row)

        print("=" * 80)

        return [

            RetrievalResult(

                score=float(row["score"]),

                chunk_id=str(row["id"]),

                repository_file_id=str(
                    row["repository_file_id"]
                ),

                chunk_name=row["chunk_name"],

                chunk_type=row["chunk_type"],

                start_line=row["start_line"],

                end_line=row["end_line"],

                content=row["content"],

            )

            for row in rows

        ]