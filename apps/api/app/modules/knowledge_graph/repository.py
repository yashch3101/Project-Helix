from sqlalchemy import or_, select

from app.modules.knowledge_graph.models import (
    SymbolRelationship,
)


class KnowledgeGraphRepository:

    @staticmethod
    async def create(
        db,
        relationship,
    ):
        db.add(relationship)
        await db.commit()
        await db.refresh(relationship)
        return relationship

    @staticmethod
    async def get_neighbors(
        db,
        symbol_id,
    ):
        result = await db.execute(
            select(SymbolRelationship).where(
                or_(
                    SymbolRelationship.from_symbol_id == symbol_id,
                    SymbolRelationship.to_symbol_id == symbol_id,
                )
            )
        )

        return result.scalars().all()