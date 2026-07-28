class ArchitectureReasoner:

    @staticmethod
    def generate(
        summary,
        modules,
        dependencies,
    ):

        architecture = []

        architecture.append("# Architecture Reasoning")
        architecture.append("")

        detected_patterns = []

        module_names = {
            module["module"].lower()
            for module in modules
        }

        framework = summary["framework"].lower()

        if (
            "frontend" in module_names
            and "backend" in module_names
        ):
            detected_patterns.append(
                "Client-Server"
            )

        if (
            "react" in framework
            or "next" in framework
        ):
            detected_patterns.append(
                "SPA Frontend"
            )

        if (
            "fastapi" in framework
            or "flask" in framework
            or "express" in framework
        ):
            detected_patterns.append(
                "REST Backend"
            )

        if summary["total_modules"] >= 5:
            detected_patterns.append(
                "Modular Architecture"
            )

        architecture.append(
            "Detected Patterns:"
        )

        if detected_patterns:

            for pattern in detected_patterns:

                architecture.append(
                    f"- {pattern}"
                )

        else:

            architecture.append(
                "- Generic Repository"
            )

        architecture.append("")

        architecture.append(
            "Repository Layers:"
        )

        if "frontend" in module_names:

            architecture.append(
                "- Frontend"
            )

        if "backend" in module_names:

            architecture.append(
                "- Backend"
            )

        architecture.append("")

        architecture.append(
            "Observations:"
        )

        if dependencies:

            architecture.append(
                "- Dependency graph available."
            )

        architecture.append(
            "- Repository analyzed successfully."
        )

        return "\n".join(architecture)