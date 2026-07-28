class ArchitectureGenerator:

    @staticmethod
    def generate(summary):

        lines = []

        lines.append("# Repository Architecture")
        lines.append("")

        lines.append(
            f"Repository Type: {summary['repository_type']}"
        )

        lines.append(
            f"Repository Type: {summary['repository_type']}"
        )

        lines.append("")

        lines.append("Modules")

        for module in summary["important_modules"]:

            lines.append(
                f"- {module}"
            )

        lines.append("")

        lines.append("Entry Points")

        for entry in summary["entry_points"]:

            lines.append(
                f"- {entry}"
            )

        return "\n".join(lines)