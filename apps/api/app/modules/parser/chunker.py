from pathlib import Path


def chunk_file(
    file_path: str,
    chunk_size: int = 40,
):
    text = Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore",
    )

    lines = text.splitlines()

    chunks = []

    start = 0

    while start < len(lines):

        end = min(
            start + chunk_size,
            len(lines),
        )

        content = "\n".join(
            lines[start:end]
        )

        chunks.append(
            {
                "start_line": start + 1,
                "end_line": end,
                "content": content,
            }
        )

        start = end

    return chunks