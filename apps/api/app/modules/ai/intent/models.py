from dataclasses import dataclass
from enum import Enum


class IntentType(str, Enum):

    GENERAL = "general"

    FUNCTION = "function"

    CLASS = "class"

    FILE = "file"

    ARCHITECTURE = "architecture"

    DEPENDENCY = "dependency"

    DOCUMENTATION = "documentation"

    REVIEW = "review"

    BUG = "bug"

    REFACTOR = "refactor"

    EXPLAIN = "explain"

    SEARCH = "search"


@dataclass
class IntentResult:

    intent: IntentType

    entity: str | None = None

    confidence: float = 1.0