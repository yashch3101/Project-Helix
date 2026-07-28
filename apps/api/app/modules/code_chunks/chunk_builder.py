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

        ALLOWED_SYMBOLS = {
            "class",
            "function",
            "method",
            "arrow_function",
            "component",
            "hook",
        }

        for symbol in symbols:

            if symbol.symbol_type not in ALLOWED_SYMBOLS:
                continue

            start = symbol.line_start
            end = symbol.line_end

            if start <= 0:
                continue

            if end < start:
                continue

            if end > len(lines):
                end = len(lines)

            content = "\n".join(
                lines[start - 1:end]
            )

            if not content.strip():
                continue

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

        print("=" * 80)
        print(file_path)
        print("Chunks:", len(chunks))
        print("=" * 80)

        return chunks