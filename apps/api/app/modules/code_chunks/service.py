from sqlalchemy import select, delete
from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.code_chunks.chunk_builder import ChunkBuilder
from app.modules.code_chunks.models import CodeChunk
from app.modules.code_chunks.repository import CodeChunkRepository
from app.modules.parser.models import CodeSymbol
from app.modules.repository_index.models import RepositoryFile
from app.modules.indexing.service import IndexingService


class CodeChunkService:

    @staticmethod
    async def build_chunks(
        db: AsyncSession,
        repository_id,
    ):

        files = (
            await db.execute(
                select(RepositoryFile).where(
                    RepositoryFile.repository_id == repository_id
                )
            )
        ).scalars().all()

        await db.execute(

            delete(CodeChunk).where(

                CodeChunk.repository_file_id.in_(

                    [file.id for file in files]

                )

            )

        )

        await db.commit()

        objects = []

        result = await db.execute(

            select(CodeSymbol).where(

                CodeSymbol.repository_file_id.in_(

                    [file.id for file in files]

                )

            )

        )

        all_symbols = result.scalars().all()

        symbols_by_file = defaultdict(list)

        for symbol in all_symbols:

            symbols_by_file[symbol.repository_file_id].append(symbol)

        print("=" * 80)
        print("FILES:", len(files))
        print("SYMBOLS:", len(all_symbols))
        print("=" * 80)

        from collections import Counter

        counter = Counter(
            symbol.symbol_type
            for symbol in all_symbols
        )

        print("=" * 80)
        print("SYMBOL TYPES")

        for k, v in sorted(counter.items()):
            print(f"{k}: {v}")

        print("=" * 80)

        for file in files:

            print(
                f"{file.file_name} -> {len(symbols_by_file[file.id])} symbols"
            )

            for s in symbols_by_file[file.id]:
                print(
                    s.symbol_name,
                    "->",
                    s.symbol_type,
                )

            chunks = ChunkBuilder.build(

                file.absolute_path,

                symbols_by_file[file.id],

            )

            print(
                f"{file.file_name} -> {len(chunks)} chunks"
            )

            for chunk in chunks:

                objects.append(

                    CodeChunk(

                        repository_file_id=file.id,

                        symbol_id=chunk["symbol_id"],

                        chunk_name=chunk["chunk_name"],

                        chunk_type=chunk["chunk_type"],

                        start_line=chunk["start_line"],

                        end_line=chunk["end_line"],

                        content=chunk["content"],

                        token_count=chunk["token_count"],

                    )

                )

        await CodeChunkRepository.save_all(
            db,
            objects,
        )

        await IndexingService.rebuild(

            db=db,

            repository_id=repository_id,

        )

        return len(objects)