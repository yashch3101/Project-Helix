from app.modules.context_compression.compressor import (
    ContextCompressor,
)

from app.modules.context_compression.budget import (
    TokenBudget,
)


class ContextCompressionPipeline:

    @staticmethod
    def run(chunks):

        # Stage 1
        chunks = ContextCompressor.compress(
            chunks
        )

        chunks = TokenBudget.apply(
            chunks,
            max_chunks=15,
        )

        return chunks