from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Integer,
    Text,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base_model import BaseModel


class CodeChunk(BaseModel):
    __tablename__ = "code_chunks"

    repository_file_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "repository_files.id",
            ondelete="CASCADE",
        )
    )

    symbol_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "code_symbols.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    chunk_type: Mapped[str] = mapped_column(
        String(50)
    )

    chunk_name: Mapped[str] = mapped_column(
        String(255)
    )

    start_line: Mapped[int] = mapped_column(
        Integer
    )

    end_line: Mapped[int] = mapped_column(
        Integer
    )

    content: Mapped[str] = mapped_column(
        Text
    )

    token_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )