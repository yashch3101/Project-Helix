class EvidenceBuilder:

    @staticmethod
    def build(reasoning):

        evidence = []

        visited = set()

        # Primary Retrieval Evidence

        for chunk in reasoning["retrieval"]:

            key = (
                chunk["chunk_name"],
                chunk["start_line"],
                chunk["end_line"],
            )

            if key in visited:
                continue

            visited.add(key)

            evidence.append({

                "type": "retrieval",

                "symbol": chunk["chunk_name"],

                "chunk_type": chunk["chunk_type"],

                "lines": (
                    f'{chunk["start_line"]}-'
                    f'{chunk["end_line"]}'
                ),

            })

        return evidence