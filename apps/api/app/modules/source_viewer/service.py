from pathlib import Path

from app.modules.source_viewer.repository import (
    SourceViewerRepository,
)


class SourceViewerService:

    @staticmethod
    async def get_source(
        db,
        symbol_id,
    ):

        symbol = await SourceViewerRepository.get_symbol(
            db,
            symbol_id,
        )

        if symbol is None:
            return None

        file = await SourceViewerRepository.get_file(
            db,
            symbol.repository_file_id,
        )

        if file is None:
            return None

        path = Path(file.absolute_path)

        lines = path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines()

        snippet = "\n".join(
            lines[
                symbol.line_start - 1:
                symbol.line_end
            ]
        )

        return {

            "symbol_id": str(symbol.id),

            "symbol_name": symbol.symbol_name,

            "file": file.relative_path,

            "start_line": symbol.line_start,

            "end_line": symbol.line_end,

            "code": snippet,
        }