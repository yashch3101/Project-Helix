from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.code_chunks.models import CodeChunk
from app.modules.embeddings.batch import batches
from app.modules.embeddings.embedder import Embedder
from app.modules.embeddings.models import CodeEmbedding
from app.modules.embeddings.repository import EmbeddingRepository


class EmbeddingService:

    BATCH_SIZE = 100

    @staticmethod
    async def generate(db: AsyncSession):

        existing = (
            await db.execute(
                select(CodeEmbedding.chunk_id)
            )
        ).scalars().all()

        print("Existing embeddings:", len(existing))

        existing = set(existing)

        chunks = (
            await db.execute(
                select(CodeChunk)
            )
        ).scalars().all()

        print("All chunks:", len(chunks))

        chunks = [
            c
            for c in chunks
            if c.id not in existing
        ]

        print("Chunks to embed:", len(chunks))

        total = 0

        for batch in batches(
            chunks,
            EmbeddingService.BATCH_SIZE,
        ):

            print("Batch Size:", len(batch))

            texts = [
                item.content
                for item in batch
            ]

            vectors = Embedder.encode_batch(
                texts
            )

            print("=" * 80)
            print("Batch Size:", len(batch))
            print("Vectors Generated:", len(vectors))

            if len(vectors) > 0:
                print("Embedding Dimension:", len(vectors[0]))

            print("=" * 80)

            embeddings = []

            for chunk, vector in zip(
                batch,
                vectors,
            ):

                embeddings.append(
                    CodeEmbedding(
                        chunk_id=chunk.id,
                        embedding=vector,
                    )
                )

            print("Embeddings Ready To Insert:", len(embeddings))

            await EmbeddingRepository.bulk_insert(
                db,
                embeddings,
            )

            total += len(batch)

            print(f"Embedded {total}")

        return total