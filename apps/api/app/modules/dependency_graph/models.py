from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class CodeDependency(BaseModel):
    __tablename__ = "code_dependencies"

    source_symbol_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "code_symbols.id",
            ondelete="CASCADE",
        ),
        nullable=True,
    )

    target_name: Mapped[str] = mapped_column(
        String(255),
    )

    dependency_type: Mapped[str] = mapped_column(
        String(255),
    )

    source_file_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "repository_files.id",
            ondelete="CASCADE",
        )
    )