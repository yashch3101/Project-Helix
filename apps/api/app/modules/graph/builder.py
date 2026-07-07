from app.modules.graph.models import GraphEdge


class GraphBuilder:

    @staticmethod
    def build(
        repository_id,
        symbols,
    ):

        edges = []

        for symbol in symbols:

            # Parent Relationship
            if symbol.parent:

                edges.append(
                    GraphEdge(
                        repository_id=repository_id,
                        source_symbol=symbol.parent,
                        relation="CONTAINS",
                        target_symbol=symbol.symbol_name,
                    )
                )

            # Inheritance Relationship
            if (
                symbol.symbol_type == "class"
                and symbol.inherits
            ):

                for base in symbol.inherits:

                    edges.append(
                        GraphEdge(
                            repository_id=repository_id,
                            source_symbol=symbol.symbol_name,
                            relation="INHERITS",
                            target_symbol=base,
                        )
                    )

            # Import Relationship
            if symbol.symbol_type == "import":

                edges.append(
                    GraphEdge(
                        repository_id=repository_id,
                        source_symbol="FILE",
                        relation="IMPORTS",
                        target_symbol=symbol.symbol_name,
                    )
                )

            # Call Relationship
            if symbol.symbol_type == "call":

                edges.append(
                    GraphEdge(
                        repository_id=repository_id,
                        source_symbol=symbol.parent,
                        relation="CALLS",
                        target_symbol=symbol.symbol_name,
                    )
                )

        return edges