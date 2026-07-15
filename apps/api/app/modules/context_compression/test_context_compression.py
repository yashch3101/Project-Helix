from app.modules.context_compression.service import (
    ContextCompressionService,
)

chunks = []

for i in range(30):

    chunks.append({

        "chunk_id": str(i),

        "content": f"Chunk {i}",

    })

compressed = ContextCompressionService.compress(
    chunks
)

print("=" * 80)

print("INPUT :", len(chunks))

print("OUTPUT:", len(compressed))

print("=" * 80)

for chunk in compressed:

    print(chunk)