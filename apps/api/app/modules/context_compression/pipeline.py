from app.modules.context_compression.compressor import (
    ContextCompressor,
)


class ContextCompressionPipeline:

    @staticmethod
    def run(chunks):

        # Stage 1
        chunks = ContextCompressor.compress(
            chunks
        )

        return chunks