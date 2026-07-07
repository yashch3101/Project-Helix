from uuid import UUID

from pydantic import BaseModel


class AIQuestion(BaseModel):

    repository_id: UUID
    question: str

class AIAnswer(BaseModel):

    answer: str