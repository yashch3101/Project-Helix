class TraceBuilder:

    @staticmethod
    def build(reasoning):

        graph = reasoning["graph"]

        nodes = {}

        edges = []

        for edge in graph:

            nodes[edge.source_symbol] = {

                "id": edge.source_symbol,

                "label": edge.source_symbol,

                "type": getattr(edge, "source_type", "Function"),

                "file_path": getattr(edge, "source_file", ""),

                "start_line": getattr(edge, "source_start_line", None),

                "end_line": getattr(edge, "source_end_line", None),

                "description": getattr(edge, "source_description", ""),

            }

            nodes[edge.target_symbol] = {

                "id": edge.target_symbol,

                "label": edge.target_symbol,

                "type": getattr(edge, "target_type", "Function"),

                "file_path": getattr(edge, "target_file", ""),

                "start_line": getattr(edge, "target_start_line", None),

                "end_line": getattr(edge, "target_end_line", None),

                "description": getattr(edge, "target_description", ""),

            }

            edges.append({

                "source": edge.source_symbol,

                "target": edge.target_symbol,

                "relation": edge.relation,

            })

        return {

            "retrieval_chunks": len(reasoning["retrieval"]),

            "graph_edges": len(graph),

            "dependencies": len(reasoning["dependency"]),

            "context_chunks": len(reasoning["context"]),

            "graph_nodes": list(nodes.values()),

            "graph_connections": edges,

        }