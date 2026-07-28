from abc import ABC, abstractmethod

from .models import ToolResult


class BaseTool(ABC):

    name: str

    @abstractmethod
    async def execute(
        self,
        db,
        repository_id,
        query: str,
        plan=None,
    ) -> ToolResult:
        pass