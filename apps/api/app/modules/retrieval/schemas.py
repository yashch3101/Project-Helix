from pydantic import BaseModel
from uuid import UUID


class SearchRequest(BaseModel):
    repository_id: UUID
    query: str
    top_k: int = 10


class SearchResult(BaseModel):
    chunk_id: UUID
    score: float
    chunk_name: str
    chunk_type: str
    content: str