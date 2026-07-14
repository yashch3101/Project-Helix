from app.modules.retrieval.vector_search import VectorSearch
from app.modules.retrieval.bm25_search import BM25Search
from app.modules.retrieval.rrf import ReciprocalRankFusion
from app.modules.retrieval.config import (
    VECTOR_TOP_K,
    BM25_TOP_K,
    RERANK_TOP_K
)
from app.modules.retrieval.reranker.service import RerankerService


class HybridSearch:

    @staticmethod
    async def search(
        db,
        repository_id,
        query,
        top_k=10,
    ):

        vector = await VectorSearch.search(

            db=db,

            repository_id=repository_id,

            query=query,

            top_k=VECTOR_TOP_K

        )

        print("VECTOR OBJECTS:", len(vector))

        bm25 = await BM25Search.search(

            db=db,

            repository_id=repository_id,

            query=query,

            top_k=BM25_TOP_K

        )
        print("BM25 OBJECTS:", len(bm25))

        vector = [

            {

                "score": x.score,

                "chunk_id": x.chunk_id,

                "repository_file_id": x.repository_file_id,

                "chunk_name": x.chunk_name,

                "chunk_type": x.chunk_type,

                "start_line": x.start_line,

                "end_line": x.end_line,

                "content": x.content,

            }

            for x in vector

        ]
        
        print("VECTOR AFTER CONVERT:", len(vector))

        merged = ReciprocalRankFusion.fuse(

            vector,

            bm25,

        )

        reranked = RerankerService.rerank(

            query,

            merged,

        )

        print("=" * 80)
        print("RERANKED SAMPLE")
        print(reranked[0])
        print("HAS repository_file_id:", "repository_file_id" in reranked[0])
        print("=" * 80)

        print("=" * 80)
        print("VECTOR RESULTS")
        for item in vector:
            print(item["chunk_name"], item["score"])

        print("=" * 80)
        print("BM25 RESULTS")
        for item in bm25:
            print(item["chunk_name"])

        print("=" * 80)
        print("FINAL RESULTS")
        for item in reranked:
            print(item["chunk_name"])

        return reranked[:RERANK_TOP_K]