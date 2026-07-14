from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.retrieval.types import RetrievalResult


class RetrievalStrategy(ABC):

    @abstractmethod
    async def search(
        self,
        db: AsyncSession,
        repository_id,
        query: str,
        top_k: int,
    ) -> list[RetrievalResult]:
        ...