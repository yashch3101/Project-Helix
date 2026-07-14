class TraceBuilder:

    @staticmethod
    def build(reasoning):

        return {

            "retrieval_chunks": len(

                reasoning["retrieval"]
            ),

            "graph_edges": len(

                reasoning["graph"]
            ),

            "dependencies": len(

                reasoning["dependency"]
            ),

            "context_chunks": len(

                reasoning["context"]

            ),
            
        }