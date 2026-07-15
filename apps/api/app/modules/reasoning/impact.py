class ImpactAnalyzer:

    @staticmethod
    def analyze(reasoning):

        impacts = []

        visited = set()

        for edge in reasoning["graph"]:

            key = (
                edge.source_symbol,
                edge.target_symbol,
            )

            if key in visited:
                continue

            visited.add(key)

            impacts.append({

                "from": edge.source_symbol,

                "to": edge.target_symbol,

                "relation": edge.relation,

            })

        return impacts