from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class RepositoryFile(BaseModel):
    __tablename__ = "repository_files"

    repository_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "repositories.id",
            ondelete="CASCADE",
        )
    )

    path: Mapped[str] = mapped_column(
        String(1000)
    )

    filename: Mapped[str] = mapped_column(
        String(255)
    )

    extension: Mapped[str] = mapped_column(
        String(30)
    )

    language: Mapped[str] = mapped_column(
        String(100)
    )

    size: Mapped[int] = mapped_column(
        Integer
    )