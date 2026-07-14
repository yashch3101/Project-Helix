from app.modules.retrieval.cache.bm25_cache import BM25Cache
from app.modules.retrieval.bm25_index import BM25Index
from app.modules.retrieval.repository import RetrievalRepository


class IndexingService:

    @staticmethod
    async def rebuild(
        db,
        repository_id,
    ):

        chunks = await RetrievalRepository.load_all_chunks(

            db=db,

            repository_id=repository_id,

        )

        bm25 = BM25Index.build(
            chunks
        )

        BM25Cache.set(

            repository_id,

            bm25,

            chunks,

        )