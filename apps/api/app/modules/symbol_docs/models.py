from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base_model import BaseModel


class SymbolDocumentation(BaseModel):
    __tablename__ = "symbol_documentation"

    symbol_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "code_symbols.id",
            ondelete="CASCADE",
        ),
        unique=True,
    )

    summary: Mapped[str] = mapped_column(
        Text,
    )

    explanation: Mapped[str] = mapped_column(
        Text,
    )

    parameters: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    returns: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    examples: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )