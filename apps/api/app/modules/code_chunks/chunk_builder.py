from pathlib import Path


class ChunkBuilder:

    @staticmethod
    def build(file_path: str, symbols: list):

        path = Path(file_path)

        if not path.exists():
            return []

        lines = path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines()

        chunks = []

        for symbol in symbols:

            start = symbol.line_start
            end = symbol.line_end

            content = "\n".join(
                lines[start - 1:end]
            )

            chunks.append(
                {
                    "chunk_name": symbol.symbol_name,
                    "chunk_type": symbol.symbol_type,
                    "start_line": start,
                    "end_line": end,
                    "content": content,
                    "token_count": len(content.split()),
                    "symbol_id": symbol.id,
                }
            )

        return chunks