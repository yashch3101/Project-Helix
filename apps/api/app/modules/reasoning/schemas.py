from uuid import UUID

from pydantic import BaseModel


class ReasoningRequest(BaseModel):

    repository_id: UUID

    query: str

    top_k: int = 10