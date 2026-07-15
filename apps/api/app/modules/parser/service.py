import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.parser.models import CodeSymbol
from app.modules.parser.python_ast_parser import PythonParser
from app.modules.parser.repository import ParserRepository
from app.modules.repository_index.models import RepositoryFile

from app.modules.symbol_docs.service import (
    SymbolDocumentationService,
)

from app.modules.symbol_docs.utils import (
    extract_symbol_code,
)

from app.modules.parser.factory import ParserFactory


class ParserService:

    @staticmethod
    async def parse_repository(
        db: AsyncSession,
        repository_id,
    ):

        print("=" * 80)
        print("PARSER STARTED")
        print(repository_id)
        print("=" * 80)

        result = await db.execute(
            select(RepositoryFile).where(
                RepositoryFile.repository_id == repository_id
            )
        )

        files = result.scalars().all()

        print("=" * 80)
        print("TOTAL FILES:", len(files))
        for f in files:
            print(
                f.file_name,
                f.extension,
                f.absolute_path
            )
        print("=" * 80)

        parsed = []

        for file in files:

            parser = ParserFactory.get_parser(
                file.extension
            )

            if parser is None:
                continue

            symbols = parser.parse(
                file.absolute_path
            )

            print("=" * 80)
            print("FILE:", file.file_name)
            print("SYMBOLS FOUND:", len(symbols))
            print("=" * 80)

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

                print("=" * 80)
                print("GENERATING DOC FOR:", symbol.symbol_name)
                print("=" * 80)

                # ----------------------------------------
                # Generate AI Documentation
                # ----------------------------------------

                source = extract_symbol_code(
                    file.absolute_path,
                    symbol.line_start,
                    symbol.line_end,
                )

                await SymbolDocumentationService.get_or_generate(
                    db=db,
                    symbol=symbol,
                    source_code=source,
                )

                parsed.append(symbol)

        return parsed