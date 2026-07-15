from sqlalchemy import select

from app.modules.parser.models import CodeSymbol
from app.modules.repository_index.models import RepositoryFile


class SourceViewerRepository:

    @staticmethod
    async def get_symbol(
        db,
        symbol_id,
    ):
        result = await db.execute(
            select(CodeSymbol).where(
                CodeSymbol.id == symbol_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_file(
        db,
        repository_file_id,
    ):
        result = await db.execute(
            select(RepositoryFile).where(
                RepositoryFile.id == repository_file_id
            )
        )

        return result.scalar_one_or_none()