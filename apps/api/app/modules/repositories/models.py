from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseModel
from app.modules.projects.models import Project


class Repository(BaseModel):
    __tablename__ = "repositories"

    name: Mapped[str] = mapped_column(String(255))

    github_url: Mapped[str] = mapped_column(String(500))

    default_branch: Mapped[str] = mapped_column(
        String(100),
        default="main",
    )

    local_path: Mapped[str] = mapped_column(
        String(500),
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
    )

    project_id = mapped_column(
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        )
    )

    files = relationship(
            "RepositoryFile",
            back_populates="repository",
            cascade="all, delete-orphan",
        )
    
    project = relationship(Project)