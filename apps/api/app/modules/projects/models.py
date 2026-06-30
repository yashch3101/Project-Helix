from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseModel
from app.modules.auth.models import User


class Project(BaseModel):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(500))

    owner_id = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    owner = relationship(User)