from sqlalchemy import select
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

        objects = []

        for file in files:

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