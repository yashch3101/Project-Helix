from dataclasses import dataclass


@dataclass
class RetrievalResult:

    score: float

    chunk_id: str

    repository_file_id: str

    chunk_name: str

    chunk_type: str

    start_line: int

    end_line: int

    content: str