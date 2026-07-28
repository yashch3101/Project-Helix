from collections import defaultdict
from pathlib import Path


class ModuleExplainer:

    @staticmethod
    def generate(files):

        modules = defaultdict(list)

        for file in files:

            parts = Path(file.relative_path).parts

            if not parts:
                continue

            module = parts[0]

            modules[module].append(file.file_name.lower())

        result = []

        for module, file_names in sorted(modules.items()):

            responsibilities = []

            if any(
                "route" in f
                or "router" in f
                or "controller" in f
                for f in file_names
            ):
                responsibilities.append("API Endpoints")

            if any(
                f == "api.ts" or f == "api.js"
                for f in file_names
            ):
                responsibilities.append("API Client")

            if any(
                "service" in f
                for f in file_names
            ):
                responsibilities.append(
                    "Business Logic"
                )

            if any(
                "model" in f
                or "schema" in f
                for f in file_names
            ):
                responsibilities.append(
                    "Data Models"
                )

            if any(
                "page" in f
                or "layout" in f
                or "component" in f
                for f in file_names
            ):
                responsibilities.append(
                    "User Interface"
                )

            if any(
                "db" in f
                or "database" in f
                for f in file_names
            ):
                responsibilities.append(
                    "Database Access"
                )

            if not responsibilities:
                responsibilities.append(
                    "General Module"
                )

            result.append(
                {
                    "module": module,
                    "responsibilities": responsibilities,
                }
            )

        return result