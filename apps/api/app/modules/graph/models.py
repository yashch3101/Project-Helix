from uuid import UUID

from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class GraphEdge(BaseModel):
    __tablename__ = "graph_edges"

    repository_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "repositories.id",
            ondelete="CASCADE",
        )
    )

    source_symbol: Mapped[str] = mapped_column(
        String(255)
    )

    relation: Mapped[str] = mapped_column(
        String(50)
    )

    target_symbol: Mapped[str] = mapped_column(
        String(255)
    )