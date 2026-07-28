from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base_model import BaseModel


class SymbolRelationship(BaseModel):
    __tablename__ = "symbol_relationships"

    from_symbol_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "code_symbols.id",
            ondelete="CASCADE",
        ),
    )

    to_symbol_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "code_symbols.id",
            ondelete="CASCADE",
        ),
    )

    relationship: Mapped[str] = mapped_column(
        String(50),
    )