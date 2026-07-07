from uuid import UUID

from pgvector.sqlalchemy import Vector # type: ignore[import]
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class CodeEmbedding(BaseModel):
    __tablename__ = "code_embeddings"

    chunk_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "code_chunks.id",
            ondelete="CASCADE",
        ),
        unique=True,
    )

    embedding = mapped_column(
        Vector(768)
    )

    model_name: Mapped[str] = mapped_column(
        default="BAAI/bge-base-en-v1.5"
    )