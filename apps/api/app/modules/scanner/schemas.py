from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ScanRepositoryRequest(BaseModel):
    repository_id: UUID


class RepositoryFileResponse(BaseModel):
    id: UUID
    filename: str
    path: str
    extension: str
    language: str
    size: int

    model_config = ConfigDict(
        from_attributes=True
    )