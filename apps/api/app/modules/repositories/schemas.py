from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class RepositoryCreate(BaseModel):
    project_id: UUID
    github_url: HttpUrl


class RepositoryResponse(BaseModel):
    id: UUID
    name: str
    github_url: str
    default_branch: str
    status: str

    model_config = ConfigDict(from_attributes=True)