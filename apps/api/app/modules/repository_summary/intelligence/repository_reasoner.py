from collections import Counter


class RepositoryReasoner:

    @staticmethod
    def generate(
        summary,
        modules,
        dependencies,
    ):

        report = []

        report.append("# Repository Reasoning")
        report.append("")

        report.append(
            f"Repository Type: {summary['repository_type']}"
        )

        report.append(
            f"Language: {summary['language']}"
        )

        report.append(
            f"Framework: {summary['framework']}"
        )

        report.append("")

        report.append("## Modules")

        for module in modules:

            report.append(
                f"- {module['module']}"
            )

            for responsibility in module["responsibilities"]:

                report.append(
                    f"    • {responsibility}"
                )

        report.append("")

        report.append("## Dependency Overview")

        dependency_counter = Counter()

        for source, targets in dependencies.items():

            dependency_counter[source] += len(targets)

        if dependency_counter:

            report.append(
                "Most Connected Symbols:"
            )

            for symbol, count in dependency_counter.most_common(10):

                report.append(
                    f"- {symbol} ({count} dependencies)"
                )

        else:

            report.append(
                "No dependency information available."
            )

        report.append("")

        report.append("## Repository Insights")

        if summary["framework"]:

            report.append(
                f"- Built using {summary['framework']}."
            )

        if summary["repository_type"]:

            report.append(
                f"- Architecture resembles a {summary['repository_type']} project."
            )

        if summary["total_modules"] > 5:

            report.append(
                "- Repository is modular."
            )

        else:

            report.append(
                "- Repository is relatively compact."
            )

        if dependency_counter:

            report.append(
                "- Dependency graph successfully generated."
            )

        return "\n".join(report)