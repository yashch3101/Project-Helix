from sqlalchemy import select
from pathlib import Path

from app.modules.repository_index.models import RepositoryFile
from app.modules.parser.models import CodeSymbol
from app.modules.graph.models import GraphEdge


class RepositoryAnalyzer:

    @staticmethod
    async def analyze(
        db,
        repository_id,
    ):

        files = (
            await db.execute(
                select(RepositoryFile).where(
                    RepositoryFile.repository_id == repository_id
                )
            )
        ).scalars().all()


        symbols = (
            await db.execute(
                select(CodeSymbol).join(
                    RepositoryFile,
                    RepositoryFile.id == CodeSymbol.repository_file_id,
                ).where(
                    RepositoryFile.repository_id == repository_id
                )
            )
        ).scalars().all()


        graph = (
            await db.execute(
                select(GraphEdge).where(
                    GraphEdge.repository_id == repository_id
                )
            )
        ).scalars().all()


        total_files = len(files)

        total_classes = sum(
            1
            for s in symbols
            if s.symbol_type == "class"
        )

        total_functions = sum(
            1
            for s in symbols
            if s.symbol_type in (
                "function",
                "method",
            )
        )

        important_modules = RepositoryAnalyzer.detect_modules(
            files
        )

        entry_points = RepositoryAnalyzer.detect_entry_points(
            files
        )

        framework = RepositoryAnalyzer.detect_framework(
            files
        )

        language = RepositoryAnalyzer.detect_language(
            files
        )

        repository_type = (
            RepositoryAnalyzer.detect_repository_type(
                files
            )
        )

        routes = []

        for file in files:

            if "router" in file.relative_path.lower():

                routes.append(file.relative_path)


        return {

            "language": language,

            "framework": framework,

            "entry_points": entry_points,

            "api_routes": routes,

            "total_files": total_files,

            "total_classes": total_classes,

            "total_functions": total_functions,

            "repository_type": repository_type,

            "total_modules": len(important_modules),

            "important_modules": important_modules,

            "graph_nodes": len(graph),

        }

    @staticmethod
    def detect_language(files):

        extensions = {
            file.extension.lower()
            for file in files
            if file.extension
        }

        langs = []

        if ".py" in extensions:
            langs.append("Python")

        if ".ts" in extensions or ".tsx" in extensions:
            langs.append("TypeScript")

        if ".js" in extensions or ".jsx" in extensions:
            langs.append("JavaScript")

        if ".java" in extensions:
            langs.append("Java")

        return " + ".join(langs) if langs else "Unknown"

    @staticmethod
    def detect_framework(files):

        names = {
            file.file_name.lower()
            for file in files
        }

        # React + Vite
        if (
            "vite.config.js" in names
            or "vite.config.ts" in names
        ):
            return "React + Vite"

        # Next.js
        if (
            "next.config.js" in names
            or "next.config.ts" in names
        ):
            return "Next.js"

        # Django
        if "manage.py" in names:
            return "Django"

        # FastAPI
        if (
            "requirements.txt" in names
            or "pyproject.toml" in names
        ):

            for file in files:

                path = file.relative_path.replace("\\", "/").lower()

                if (
                    path.endswith("/app.py")
                    or path.endswith("/main.py")
                ):
                    return "FastAPI"

        # Express
        if "package.json" in names:

            for file in files:

                path = file.relative_path.replace("\\", "/").lower()

                if path.endswith("server.js"):

                    return "Express.js"

        return "Unknown"

    @staticmethod
    def detect_entry_points(files):

        entry_points = []

        candidates = {
            "main.py",
            "app.py",
            "__main__.py",
            "server.py",
            "main.jsx",
            "main.tsx",
            "index.js",
            "index.ts",
        }

        for file in files:

            path = file.relative_path.replace("\\", "/").lower()

            if (
                path.endswith("/main.py")
                or path.endswith("/app.py")
                or path.endswith("/server.py")
                or path.endswith("/__main__.py")
                or path.endswith("/src/main.jsx")
                or path.endswith("/src/main.tsx")
                or path.endswith("/src/index.js")
                or path.endswith("/src/index.ts")
            ):
                entry_points.append(file.relative_path)

        return entry_points

    @staticmethod
    def detect_modules(files):

        modules = set()

        for file in files:

            parts = Path(file.relative_path).parts

            if len(parts) > 1:

                modules.add(parts[0])

        return sorted(modules)

    @staticmethod
    def detect_repository_type(files):

        framework = RepositoryAnalyzer.detect_framework(files)

        names = {
            file.file_name.lower()
            for file in files
        }

        has_python = any(
            f.extension == ".py"
            for f in files
        )

        has_ts = any(
            f.extension in (
                ".ts",
                ".tsx",
            )
            for f in files
        )

        has_js = any(
            f.extension in (
                ".js",
                ".jsx",
            )
            for f in files
        )

        if framework == "Next.js" and has_python:
            return "Python Backend + Next.js Frontend"

        if framework == "React + Vite" and has_python:
            return "Python Backend + React Frontend"

        if framework == "Express.js" and has_js:
            return "Node Backend"

        if framework == "FastAPI":
            return "Python Backend"

        return "Generic Repository"