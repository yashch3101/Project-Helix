from dataclasses import dataclass


@dataclass
class GraphEdgeDTO:

    # Source symbol
    source_symbol: str
    source_type: str
    source_file: str
    source_start_line: int
    source_end_line: int
    source_docstring: str | None

    # Target symbol
    target_symbol: str
    target_type: str
    target_file: str
    target_start_line: int
    target_end_line: int
    target_docstring: str | None

    # Relationship
    relation: str