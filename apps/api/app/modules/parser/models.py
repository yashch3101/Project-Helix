from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class CodeSymbol(BaseModel):
    __tablename__ = "code_symbols"

    repository_file_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "repository_files.id",
            ondelete="CASCADE",
        )
    )

    symbol_name: Mapped[str] = mapped_column(String(255))

    symbol_type: Mapped[str] = mapped_column(String(50))

    line_start: Mapped[int] = mapped_column(Integer)

    line_end: Mapped[int] = mapped_column(Integer)

    parent: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    inherits: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    docstring: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    decorators: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    return_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    parameters: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_async: Mapped[bool] = mapped_column(
        default=False,
    )