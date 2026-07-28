from app.modules.reasoning.pipeline import ReasoningPipeline


class ReasoningService:

    @staticmethod
    async def build(
        db,
        repository_id,
        query,
    ):

        return await ReasoningPipeline.run(
            db=db,
            repository_id=repository_id,
            query=query,
        )