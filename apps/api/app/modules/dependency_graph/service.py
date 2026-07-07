from sqlalchemy import select

from app.modules.dependency_graph.models import CodeDependency
from app.modules.dependency_graph.python_dependency_parser import (
    PythonDependencyParser,
)
from app.modules.parser.models import CodeSymbol
from app.modules.repository_index.models import RepositoryFile


class DependencyService:

    @staticmethod
    async def build(
        db,
        repository_id,
    ):

        result = await db.execute(
            select(RepositoryFile).where(
                RepositoryFile.repository_id == repository_id
            )
        )

        files = result.scalars().all()

        total = 0

        for file in files:

            if file.extension != ".py":
                continue

            deps = PythonDependencyParser.parse(
                file.absolute_path,
            )

            for dep in deps:

                dependency = CodeDependency(
                    source_symbol_id=None,
                    source_file_id=file.id,
                    target_name=dep["target"],
                    dependency_type=dep["type"],
                )

                db.add(dependency)

                total += 1

        await db.commit()

        return {
            "dependencies": total,
        }