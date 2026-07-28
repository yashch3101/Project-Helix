from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:

    tool: str

    success: bool

    data: Any = None

    metadata: dict = field(default_factory=dict)

    error: str | None = None