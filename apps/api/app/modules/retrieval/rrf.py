class ReciprocalRankFusion:

    @staticmethod
    def fuse(*rankings, k=60):

        scores = {}

        documents = {}

        for ranking in rankings:

            for rank, item in enumerate(ranking):

                chunk_id = item["chunk_id"]

                documents[chunk_id] = item

                scores.setdefault(chunk_id, 0)

                scores[chunk_id] += 1 / (k + rank + 1)

        merged = sorted(

            documents.values(),

            key=lambda x: scores[x["chunk_id"]],

            reverse=True,

        )

        return merged