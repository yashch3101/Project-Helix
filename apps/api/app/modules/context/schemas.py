from uuid import UUID

from pydantic import BaseModel


class ContextRequest(BaseModel):
    repository_id: UUID
    query: str
    top_k: int = 5