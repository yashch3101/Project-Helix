from app.modules.context_compression.service import (
    ContextCompressionService,
)

chunks = [

    {
        "chunk_id": "1",
        "content": "hello",
    },

    {
        "chunk_id": "2",
        "content": "world",
    },

    {
        "chunk_id": "1",
        "content": "hello",
    },

]

compressed = ContextCompressionService.compress(
    chunks
)

print("=" * 80)

print("INPUT :", len(chunks))

print("OUTPUT:", len(compressed))

print("=" * 80)

for chunk in compressed:

    print(chunk)