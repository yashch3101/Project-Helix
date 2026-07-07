from app.modules.embeddings.embedder import Embedder
from app.modules.context.repository import ContextRepository


class ContextService:

    @staticmethod
    async def build(
        db,
        repository_id,
        query,
        top_k=5,
    ):
        query_vector = Embedder.encode(query)

        return await ContextRepository.retrieve(
            db=db,
            repository_id=repository_id,
            query_vector=query_vector,
            top_k=top_k,
        )