from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.parser.models import CodeSymbol


class ParserRepository:

    @staticmethod
    async def save(
        db: AsyncSession,
        symbol: CodeSymbol,
    ):
        db.add(symbol)
        await db.commit()
        await db.refresh(symbol)
        return symbol