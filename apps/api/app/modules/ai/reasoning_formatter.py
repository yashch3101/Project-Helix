class ReasoningFormatter:

    @staticmethod
    def format(reasoning):

        lines = []

        # ==========================================================
        # RETRIEVAL
        # ==========================================================

        lines.append("# RETRIEVAL RESULTS\n")

        for item in reasoning["retrieval"]:

            lines.append(
                f"""
FILE: {item["chunk_name"]}
TYPE: {item["chunk_type"]}
LINES: {item["start_line"]}-{item["end_line"]}

{item["content"]}

----------------------------------------
"""
            )

        # ==========================================================
        # GRAPH
        # ==========================================================

        lines.append("\n# GRAPH RELATIONSHIPS\n")

        for edge in reasoning["graph"]:

            lines.append(
                f"{edge.source_symbol}"
                f" --{edge.relation}--> "
                f"{edge.target_symbol}"
            )

        # ==========================================================
        # DEPENDENCIES
        # ==========================================================

        lines.append("\n# DEPENDENCIES\n")

        print("=" * 80)

        if reasoning["dependency"]:
            print("DEPENDENCY SAMPLE")
            print(reasoning["dependency"][0])
            print(type(reasoning["dependency"][0]))
        else:
            print("NO DEPENDENCIES")

        print("=" * 80)

        for dep in reasoning["dependency"]:

            lines.append(

                f"{dep.dependency_type} -> {dep.target_name}"

            )

        # ==========================================================
        # CONTEXT
        # ==========================================================

        lines.append("\n# EXPANDED CONTEXT\n")

        for chunk in reasoning["context"]:

            if isinstance(chunk, dict):

                lines.append(chunk["content"])

            else:

                lines.append(chunk.content)

        return "\n".join(lines)