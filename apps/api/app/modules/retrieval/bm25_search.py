from app.modules.retrieval.base import RetrievalStrategy
from app.modules.retrieval.cache.bm25_cache import BM25Cache
from app.modules.retrieval.tokenizer import Tokenizer
from app.modules.indexing.service import (
                IndexingService,
            )


class BM25Search(RetrievalStrategy):

    @staticmethod
    async def search(
        db,
        repository_id,
        query: str,
        top_k: int,
    ):

        cache = BM25Cache.get(repository_id)

        if cache is None:

            await IndexingService.rebuild(

                db=db,

                repository_id=repository_id,

            )

            cache = BM25Cache.get(repository_id)

            if cache is None:

                return []

        bm25 = cache["bm25"]
        chunks = cache["chunks"]

        tokens = Tokenizer.tokenize(query)

        print("QUERY:", query)
        print("TOKENS:", tokens)

        scores = bm25.get_scores(tokens)

        if len(scores) > 0:
            print("MAX SCORE:", float(scores.max()))
        else:
            print("MAX SCORE: 0")

        print(
            "NON ZERO SCORES:",
            int((scores > 0).sum())
        )

        ranked = sorted(

            zip(chunks, scores),

            key=lambda x: x[1],

            reverse=True,

        )

        results = []

        for chunk, score in ranked[:top_k]:

            results.append({

                "score": float(score),

                "chunk_id": str(chunk.id),

                "repository_file_id": str(
                    chunk.repository_file_id
                ),

                "chunk_name": chunk.chunk_name,

                "chunk_type": chunk.chunk_type,

                "start_line": chunk.start_line,

                "end_line": chunk.end_line,

                "content": chunk.content,

            })

        return results