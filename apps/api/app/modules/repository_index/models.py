from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base_model import BaseModel
from app.modules.repositories.models import Repository


class RepositoryFile(BaseModel):
    __tablename__ = "repository_files"

    repository_id: Mapped[str] = mapped_column(
        ForeignKey(
            "repositories.id",
            ondelete="CASCADE",
        )
    )

    file_name: Mapped[str] = mapped_column(
        String(255)
    )

    relative_path: Mapped[str] = mapped_column(
        String(1000)
    )

    absolute_path: Mapped[str] = mapped_column(
        String(1000)
    )

    extension: Mapped[str] = mapped_column(
        String(30)
    )

    language: Mapped[str] = mapped_column(
        String(50)
    )

    size: Mapped[int] = mapped_column(
        Integer
    )

    sha256: Mapped[str] = mapped_column(
        String(64)
    )

    modified_time: Mapped[str] = mapped_column(
        String(100)
    )

    is_parsed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    parser_version: Mapped[str] = mapped_column(
        String(30),
        default="v1",
    )

    embedding_version: Mapped[str] = mapped_column(
        String(30),
        default="v1",
    )

    repository = relationship(
        Repository,
        back_populates="files",
    )

    chunks = relationship(
        "RepositoryChunk",
        back_populates="repository_file",
        cascade="all, delete-orphan",
    )

class RepositoryChunk(BaseModel):
    __tablename__ = "repository_chunks"

    repository_file_id: Mapped[str] = mapped_column(
        ForeignKey(
            "repository_files.id",
            ondelete="CASCADE",
        )
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer
    )

    start_line: Mapped[int] = mapped_column(
        Integer
    )

    end_line: Mapped[int] = mapped_column(
        Integer
    )

    content: Mapped[str] = mapped_column(
        String
    )

    embedding_status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
    )

    repository_file = relationship(
        "RepositoryFile",
        back_populates="chunks",
    )