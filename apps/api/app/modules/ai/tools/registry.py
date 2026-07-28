from .vector_tool import VectorSearchTool
from .graph_tool import GraphSearchTool
from .dependency_tool import DependencyTool


class ToolRegistry:

    _tools = {
        "vector_search": VectorSearchTool(),
        "graph_search": GraphSearchTool(),
        "dependency_search": DependencyTool(),
    }

    @classmethod
    def get(cls, tool_name: str):
        return cls._tools.get(tool_name)