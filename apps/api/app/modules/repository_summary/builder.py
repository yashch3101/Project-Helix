class RepositorySummaryBuilder:

    @staticmethod
    def build(summary: dict) -> str:

        lines = []

        lines.append("# Repository Knowledge Card")
        lines.append("")

        lines.append(f"Repository Type: {summary['repository_type']}")
        lines.append(f"Language: {summary['language']}")
        lines.append(f"Framework: {summary['framework']}")
        lines.append("")

        lines.append('## Statistics')

        lines.append(f"Files: {summary['total_files']}")
        lines.append(f"Classes: {summary['total_classes']}")
        lines.append(f"Functions: {summary['total_functions']}")
        lines.append(f"Graph Nodes: {summary['graph_nodes']}")
        lines.append("")

        lines.append("## Entry Points")

        if summary["entry_points"]:

            for entry in summary["entry_points"]:
                lines.append(f"- {entry}")


        else:
            lines.append("- None")

        lines.append("")

        lines.append("## Important Modules")

        for module in summary["important_modules"]:
            lines.append(f"- {module}")

        lines.append("")

        lines.append("## API Routes")

        if summary["api_routes"]:

            for route in summary["api_routes"]:
                lines.append(f"- {route}")

        else:
            lines.append("- None")

        return "\n".join(lines)