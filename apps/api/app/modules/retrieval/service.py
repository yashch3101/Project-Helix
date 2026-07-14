from app.modules.retrieval.retrieval_pipeline import RetrievalPipeline


class RetrievalService:

    @staticmethod
    async def search(
        db,
        repository_id,
        query,
        top_k=10,
    ):

        results = await RetrievalPipeline.retrieve(

            db=db,

            repository_id=repository_id,

            query=query,

            top_k=top_k,

        )

        return results