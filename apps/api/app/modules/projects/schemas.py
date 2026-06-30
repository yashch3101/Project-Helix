from pydantic import BaseModel, ConfigDict
from uuid import UUID


class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)