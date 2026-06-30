from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.scanner.models import RepositoryFile


class ScannerRepository:

    @staticmethod
    async def save(
        db: AsyncSession,
        file: RepositoryFile,
    ):
        db.add(file)
        await db.commit()
        await db.refresh(file)
        return file