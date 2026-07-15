from sqlalchemy import select

from app.modules.symbol_docs.models import (
    SymbolDocumentation,
)


class SymbolDocumentationRepository:

    @staticmethod
    async def get_by_symbol(
        db,
        symbol_id,
    ):
        result = await db.execute(
            select(SymbolDocumentation).where(
                SymbolDocumentation.symbol_id == symbol_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        db,
        doc,
    ):
        db.add(doc)
        await db.commit()
        await db.refresh(doc)
        return doc