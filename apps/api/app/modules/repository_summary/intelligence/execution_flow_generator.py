class ExecutionFlowGenerator:

    @staticmethod
    def generate(summary):

        lines = []

        lines.append("# Execution Flow")
        lines.append("")

        repository_type = summary["repository_type"]

        if "Next.js" in repository_type:

            lines.extend([
                "User",
                "↓",
                "Next.js Frontend",
                "↓",
                "FastAPI Backend",
                "↓",
                "Business Logic",
                "↓",
                "Database",
            ])

        elif "React" in repository_type:

            lines.extend([
                "User",
                "↓",
                "React Frontend",
                "↓",
                "FastAPI Backend",
                "↓",
                "Business Logic",
                "↓",
                "Database",
            ])

        else:

            lines.extend([
                "User",
                "↓",
                "Application",
                "↓",
                "Business Logic",
            ])

        return "\n".join(lines)