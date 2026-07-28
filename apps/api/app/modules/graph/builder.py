from ast import literal_eval

from app.modules.graph.models import GraphEdge


class GraphBuilder:

    @staticmethod
    def build(
        repository_id,
        symbols,
    ):

        edges = []

        edge_set = set()

        def add_edge(source, relation, target):

            if not source or not target:
                return

            key = (
                source,
                relation,
                target,
            )

            if key in edge_set:
                return

            edge_set.add(key)

            edges.append(
                GraphEdge(
                    repository_id=repository_id,
                    source_symbol=source,
                    relation=relation,
                    target_symbol=target,
                )
            )

        for symbol in symbols:

            # Parent Relationship
            if symbol.parent:

                add_edge(
                    symbol.parent,
                    "CONTAINS",
                    symbol.symbol_name,
                )

            # Inheritance Relationship
            if (
                symbol.symbol_type == "class"
                and symbol.inherits
            ):

                    try:

                        bases = literal_eval(
                            symbol.inherits
                        )

                    except Exception:

                        bases = []

                    for base in bases:

                        add_edge(
                            symbol.symbol_name,
                            "INHERITS",
                            base,
                        )

            # Import Relationship
            if symbol.symbol_type == "import":

                add_edge(
                    "FILE",
                    "IMPORTS",
                    symbol.symbol_name,
                )

            # Call Relationship
            if symbol.symbol_type == "call":

                add_edge(
                    symbol.parent,
                    "CALLS",
                    symbol.symbol_name,
                )

            # Variable Definition
            if symbol.symbol_type == "variable":

                add_edge(
                    symbol.parent,
                    "DEFINES",
                    symbol.symbol_name,
                )

            # Return Relationship
            if symbol.symbol_type == "return":

                add_edge(
                    symbol.parent,
                    "RETURNS",
                    symbol.symbol_name,
                )
            
        print("=" * 80)
        print("GRAPH EDGES:", len(edges))
        print("=" * 80)

        return edges