from dataclasses import dataclass, field
from enum import Enum


class AgentType(str, Enum):

    REPOSITORY = "repository"

    REVIEW = "review"

    DOCUMENTATION = "documentation"

    BUG = "bug"

    REFACTOR = "refactor"


class ToolType(str, Enum):

    VECTOR_SEARCH = "vector_search"

    GRAPH_SEARCH = "graph_search"

    DEPENDENCY_SEARCH = "dependency_search"

    SUMMARY = "summary"

    CODE_REVIEW = "code_review"

    BUG_ANALYSIS = "bug_analysis"


@dataclass
class ExecutionPlan:

    # Which agent should execute
    agent: AgentType

    # Which tools should run
    tools: list[ToolType] = field(default_factory=list)

    # Intent
    intent: str = "GENERAL"

    entity: str | None = None

    # Retrieval Strategy
    retrieval_limit: int = 10

    expand_graph: bool = True

    expand_dependencies: bool = True

    use_context: bool = True

    use_impact: bool = False

    # Repository metadata

    retrieve_folder_structure: bool = False

    retrieve_entrypoints: bool = False

    retrieve_architecture: bool = False