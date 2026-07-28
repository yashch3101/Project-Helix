from dataclasses import dataclass


@dataclass
class RetrievalPlan:

    intent: str

    retrieval_limit: int

    expand_graph: bool

    expand_dependencies: bool

    use_context: bool

    use_impact: bool

    retrieve_folder_structure: bool

    retrieve_entrypoints: bool

    retrieve_architecture: bool


class IntentClassifier:

    @staticmethod
    def classify(query: str):

        q = query.lower()

        # -----------------------------------

        if any(x in q for x in [

            "architecture",

            "design",

            "flow",

            "pipeline",

            "folder",

            "structure",

            "overview",

            "how works"

        ]):

            return RetrievalPlan(

                intent="ARCHITECTURE",

                retrieval_limit=15,

                expand_graph=True,

                expand_dependencies=True,

                use_context=True,

                use_impact=False,

                retrieve_folder_structure=True,

                retrieve_entrypoints=True,

                retrieve_architecture=True,

            )

        # -----------------------------------

        if any(x in q for x in [

            "bug",

            "fix",

            "error",

            "exception",

            "issue"

        ]):

            return RetrievalPlan(

                intent="DEBUG",

                retrieval_limit=20,

                expand_graph=True,

                expand_dependencies=True,

                use_context=True,

                use_impact=True,

                retrieve_folder_structure=False,

                retrieve_entrypoints=False,

                retrieve_architecture=False,

            )

        # -----------------------------------

        if any(x in q for x in [

            "dependency",

            "depends",

            "caller",

            "callee"

        ]):

            return RetrievalPlan(

                intent="DEPENDENCY",

                retrieval_limit=20,

                expand_graph=True,

                expand_dependencies=True,

                use_context=False,

                use_impact=True,

                retrieve_folder_structure=False,

                retrieve_entrypoints=False,

                retrieve_architecture=False,

            )

        # -----------------------------------

        return RetrievalPlan(

            intent="GENERAL",

            retrieval_limit=10,

            expand_graph=True,

            expand_dependencies=True,

            use_context=True,

            use_impact=False,

            retrieve_folder_structure=False,

            retrieve_entrypoints=False,

            retrieve_architecture=False,

        )