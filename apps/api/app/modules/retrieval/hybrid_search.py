from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.modules.retrieval.vector_search import VectorSearch
from app.modules.retrieval.bm25_search import BM25Search
from app.modules.retrieval.rrf import ReciprocalRankFusion
from app.modules.retrieval.config import (
    VECTOR_TOP_K,
    BM25_TOP_K,
)
from app.modules.retrieval.reranker.service import RerankerService
import re

TOKEN_REGEX = re.compile(
    r"[A-Za-z_][A-Za-z0-9_]*"
)

import logging

logger = logging.getLogger(__name__)

class HybridSearch:

    @staticmethod
    async def search(
        db: AsyncSession,
        repository_id: UUID,
        query: str,
        top_k: int = 10,
    ):

        vector = await VectorSearch.search(

            db=db,

            repository_id=repository_id,

            query=query,

            top_k=VECTOR_TOP_K

        )

        logger.debug("VECTOR OBJECTS: %s", len(vector))

        bm25 = await BM25Search.search(

            db=db,

            repository_id=repository_id,

            query=query,

            top_k=BM25_TOP_K

        )

        logger.debug("BM25 OBJECTS: %s", len(bm25))

        vector = [

            {

                "score": x.score,

                "chunk_id": x.chunk_id,

                "repository_file_id": x.repository_file_id,

                "file_name": x.file_name,

                "relative_path": x.relative_path,

                "chunk_name": x.chunk_name,

                "chunk_type": x.chunk_type,

                "start_line": x.start_line,

                "end_line": x.end_line,

                "content": x.content,

            }

            for x in vector

        ]
        
        logger.debug("VECTOR AFTER CONVERT: %s", len(vector))

        merged = ReciprocalRankFusion.fuse(

            vector,

            bm25,

        )

        # ----------------------------------------
        # Exact Symbol Boost
        # ----------------------------------------

        tokens = TOKEN_REGEX.findall(
            query
        )

        token_set = {
            t.lower()
            for t in tokens
        }

        for item in merged:

            chunk_name = item["chunk_name"].lower()

            if chunk_name in token_set:

                item["score"] += 100

        reranked = RerankerService.rerank(
            query,
            merged,
        )

        logger.debug("FINAL RERANKED RESULTS")

        for item in reranked[:10]:

            logger.debug(
                "%s | score=%s | rerank=%s",
                item["chunk_name"],
                item.get("score"),
                item.get("rerank_score"),
            )

        return reranked[:top_k]