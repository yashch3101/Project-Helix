from app.modules.context_compression.pipeline import (
    ContextCompressionPipeline,
)


class ContextCompressionService:

    @staticmethod
    def compress(chunks):

        return ContextCompressionPipeline.run(
            chunks
        )