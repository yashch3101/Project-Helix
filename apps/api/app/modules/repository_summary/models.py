from uuid import uuid4

from sqlalchemy import (
    String,
    Integer,
    Text,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base_model import BaseModel


class RepositorySummary(BaseModel):

    __tablename__ = "repository_summaries"

    repository_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "repositories.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    language: Mapped[str] = mapped_column(String)

    framework: Mapped[str] = mapped_column(String)

    repository_type: Mapped[str] = mapped_column(String)

    entry_points: Mapped[str] = mapped_column(Text)

    api_routes: Mapped[str] = mapped_column(Text)

    total_files: Mapped[int] = mapped_column(Integer)

    total_classes: Mapped[int] = mapped_column(Integer)

    total_functions: Mapped[int] = mapped_column(Integer)

    total_modules: Mapped[int] = mapped_column(Integer)

    important_modules: Mapped[str] = mapped_column(Text)

    architecture: Mapped[str] = mapped_column(Text)

    execution_flow: Mapped[str] = mapped_column(Text)

    knowledge_card: Mapped[str] = mapped_column(Text)