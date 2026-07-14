from pathlib import Path


class CodeSplitter:

    CHUNK_SIZE = 40

    @staticmethod
    def split(file_path: str):

        text = Path(file_path).read_text(
            encoding="utf-8",
            errors="ignore",
        )

        lines = text.splitlines()

        chunks = []

        for start in range(
            0,
            len(lines),
            CodeSplitter.CHUNK_SIZE,
        ):

            end = min(
                start + CodeSplitter.CHUNK_SIZE,
                len(lines),
            )

            chunks.append(
                {
                    "content": "\n".join(
                        lines[start:end]
                    ),
                    "start_line": start + 1,
                    "end_line": end,
                }
            )

        return chunks