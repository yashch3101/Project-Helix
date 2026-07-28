from dataclasses import dataclass


@dataclass
class RewrittenQuery:

    original: str

    rewritten: str


class QueryRewriter:

    @staticmethod
    def rewrite(query: str):

        q = query.lower()

        # ----------------------------
        # Architecture
        # ----------------------------

        if "architecture" in q:

            rewritten = (
                query
                + "\n"
                + "Explain repository architecture, "
                  "entry point, execution flow, "
                  "important modules, folder structure."
            )

        # ----------------------------
        # Bug
        # ----------------------------

        elif "bug" in q or "error" in q:

            rewritten = (
                query
                + "\n"
                + "Find root cause, affected functions, "
                  "dependency chain and possible fixes."
            )

        # ----------------------------
        # Callers
        # ----------------------------

        elif "called" in q:

            rewritten = (
                query
                + "\n"
                + "Find all callers, references and call hierarchy."
            )

        # ----------------------------
        # Default
        # ----------------------------

        else:

            rewritten = query

        return RewrittenQuery(

            original=query,

            rewritten=rewritten,

        )