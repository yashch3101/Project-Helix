class ImpactFormatter:

    @staticmethod
    def format(result):

        lines = []

        lines.append(
            f"Impact Analysis for {result['symbol']}\n"
        )

        lines.append("Called By:")

        if result["callers"]:

            for caller in result["callers"]:

                lines.append(
                    f"• {caller}"
                )

        else:

            lines.append(
                "• No callers"
            )

        lines.append("\nCalls:")

        if result["callees"]:

            for callee in result["callees"]:

                lines.append(
                    f"• {callee}"
                )

        else:

            lines.append(
                "• No outgoing calls"
            )

        return "\n".join(lines)