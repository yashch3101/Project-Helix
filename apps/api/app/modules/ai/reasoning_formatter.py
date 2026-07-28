class ReasoningFormatter:

    @staticmethod
    def format(reasoning):

        lines = []

        # ==========================================================
        # RETRIEVAL
        # ==========================================================

        lines.append("# RETRIEVAL RESULTS\n")

        MAX_RETRIEVAL = 2

        for item in reasoning["retrieval"][:MAX_RETRIEVAL]:

            content = item["content"]

            MAX_CONTENT_CHARS = 500

            if len(content) > MAX_CONTENT_CHARS:
                content = content[:MAX_CONTENT_CHARS] + "\n..."

            lines.append(
                f"""
        FILE: {item["chunk_name"]}
        TYPE: {item["chunk_type"]}
        LINES: {item["start_line"]}-{item["end_line"]}

        {content}

        ----------------------------------------
        """
            )

        # ==========================================================
        # GRAPH
        # ==========================================================

        lines.append("\n# GRAPH RELATIONSHIPS\n")

        MAX_GRAPH = 8

        for edge in reasoning["graph"][:MAX_GRAPH]:

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

        MAX_DEPENDENCIES = 8

        for dep in reasoning["dependency"][:MAX_DEPENDENCIES]:

            lines.append(

                f"{dep.dependency_type} -> {dep.target_name}"

            )

        formatted = "\n".join(lines)

        print("=" * 80)
        print("FORMATTED CONTEXT CHARS:", len(formatted))
        print("=" * 80)

        return formatted