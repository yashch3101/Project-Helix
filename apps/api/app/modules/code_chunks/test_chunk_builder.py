from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.modules.code_chunks.chunk_builder import ChunkBuilder
from app.modules.parser.models import CodeSymbol
from app.modules.repository_index.models import RepositoryFile


async def main():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(RepositoryFile).where(
                RepositoryFile.id ==
                "04fd4540-eede-4d78-8a83-74b61b31f292"
            )
        )

        file = result.scalar_one()

        symbols = (
            await db.execute(
                select(CodeSymbol).where(
                    CodeSymbol.repository_file_id == file.id
                )
            )
        ).scalars().all()

        chunks = ChunkBuilder.build(
            file.absolute_path,
            symbols,
        )

        print("Chunks:", len(chunks))

        for chunk in chunks[:5]:
            print("=" * 50)
            print(chunk["chunk_name"])
            print(chunk["chunk_type"])
            print(chunk["start_line"], "-", chunk["end_line"])
            print(chunk["content"][:300])


if __name__ == "__main__":

    import asyncio

    asyncio.run(main())