from .builder import RepositoryContext


class RepositoryContextFormatter:

    @staticmethod
    def format(
        context: RepositoryContext,
    ) -> str:

        sections = []

        # -------------------
        # VECTOR
        # -------------------

        if context.vector_results:

            sections.append("## Relevant Code\n")

            for chunk in context.vector_results:
                print(chunk)

                print("=" * 80)
                print("RELATIVE PATH:", chunk.get("relative_path"))
                print("FILE NAME:", chunk.get("file_name"))
                print("KEYS:", chunk.keys())
                print("=" * 80)

                sections.append(
                    f"""
                Function: {chunk['chunk_name']}
                Type: {chunk['chunk_type']}
                Repository File:
                {chunk.get("relative_path", "Repository file path not available")}

                Start Line:
                {chunk['start_line']}

                End Line:
                {chunk['end_line']}

                Source Code:

                ```python
                {chunk['content']}
                ```
            """
            )

        # -------------------
        # GRAPH
        # -------------------

        if context.graph_results:

            sections.append("\n## Graph Relationships\n")

            seen = set()

            ALLOWED = {
                "CALLS",
                "RETURNS",
                "DEFINES",
                "IMPORTS",
                "INHERITS",
            }

            for edge in context.graph_results:

                if edge.relation not in ALLOWED:
                    continue

                key = (
                    edge.source_symbol,
                    edge.relation,
                    edge.target_symbol,
                )

                if key in seen:
                    continue

                seen.add(key)

                sections.append(
                    f"""
                {edge.source_symbol}
                --{edge.relation}-->
                {edge.target_symbol}

                Source File:
                {edge.source_file}

                Target File:
                {edge.target_file}
                """
                )

        # -------------------
        # DEPENDENCIES
        # -------------------

        if context.dependency_results:

            sections.append("\n## Dependencies\n")

            seen = set()

            for dep in context.dependency_results:

                if dep in seen:
                    continue

                seen.add(dep)

                sections.append(f"- {dep}")

        return "\n".join(sections)