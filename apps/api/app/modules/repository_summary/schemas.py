from pydantic import BaseModel


class RepositorySummarySchema(BaseModel):

    repository_type: str

    language: str

    framework: str

    entry_points: str

    api_routes: str

    total_files: int

    total_classes: int

    total_functions: int

    total_modules: int

    important_modules: str

    architecture: str

    execution_flow: str

    knowledge_card: str