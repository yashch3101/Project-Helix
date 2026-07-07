from pydantic import BaseModel
from uuid import UUID


class ChunkRequest(BaseModel):
    repository_id: UUID