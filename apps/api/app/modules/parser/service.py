import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.parser.models import CodeSymbol
from app.modules.parser.python_ast_parser import PythonParser
from app.modules.parser.repository import ParserRepository
from app.modules.repository_index.models import RepositoryFile


class ParserService:

    @staticmethod
    async def parse_repository(
        db: AsyncSession,
        repository_id,
    ):

        result = await db.execute(
            select(RepositoryFile).where(
                RepositoryFile.repository_id == repository_id
            )
        )

        files = result.scalars().all()

        parsed = []

        for file in files:

            if file.extension != ".py":
                continue

            if not os.path.exists(file.absolute_path):
                continue

            symbols = PythonParser.parse(
                file.absolute_path
            )

            for item in symbols:

                print("=" * 80)
                print("NAME:", item["name"], len(str(item["name"] or "")))
                print("TYPE:", item["type"], len(str(item["type"] or "")))
                print("PARENT:", item["parent"], len(str(item["parent"] or "")))
                print("RETURN:", item["return_type"], len(str(item["return_type"] or "")))
                print("INHERITS:", len(str(item["inherits"] or "")))
                print("DECORATORS:", len(str(item["decorators"] or "")))
                print("PARAMETERS:", len(str(item["parameters"] or "")))
                print("DOCSTRING:", len(str(item["docstring"] or "")))
                print("=" * 80)

                symbol = CodeSymbol(
                    repository_file_id=file.id,
                    symbol_name=item["name"],
                    symbol_type=item["type"],
                    line_start=item["line_start"],
                    line_end=item["line_end"],
                    parent=item["parent"],
                    inherits=str(item["inherits"]),
                    docstring=item["docstring"],
                    decorators=str(item["decorators"]),
                    parameters=str(item["parameters"]),
                    return_type=item["return_type"],
                    is_async=item["is_async"],
                )

                symbol = await ParserRepository.save(
                    db,
                    symbol,
                )

                parsed.append(symbol)

        return parsed