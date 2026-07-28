from pathlib import Path

LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
}

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
}

IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    ".venv",
    "venv",
}

class FileScanner:

    @staticmethod
    def scan(repository_path: str):

        files = []

        root = Path(repository_path)

        for path in root.rglob("*"):

            if any(part in IGNORE_DIRS for part in path.parts):
                continue

            if not path.is_file():
                continue

            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            files.append(
                {
                    "name": path.name,
                    "extension": path.suffix,
                    "language": LANGUAGE_MAP.get(
                        path.suffix.lower(),
                        "Unknown",
                    ),
                    "absolute_path": str(path),
                    "relative_path": str(path.relative_to(root)),
                    "size": path.stat().st_size,
                }
            )

        return files