class CitationBuilder:

    @staticmethod
    def build(retrieval):

        citations = []

        seen = set()

        for item in retrieval:

            key = (
                item["chunk_name"],
                item["start_line"],
                item["end_line"],
            )

            if key in seen:
                continue

            seen.add(key)

            citations.append(
                {
                    "file": item["chunk_name"],
                    "type": item["chunk_type"],
                    "start_line": item["start_line"],
                    "end_line": item["end_line"],
                    "score": round(item["score"], 3),
                }
            )

        return citations