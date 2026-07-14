from sentence_transformers import CrossEncoder


class RerankerService:

    _model = None

    @classmethod
    def model(cls):

        if cls._model is None:

            cls._model = CrossEncoder(

                "cross-encoder/ms-marco-MiniLM-L-6-v2"

            )

        return cls._model

    @classmethod
    def rerank(
        cls,
        query,
        documents,
    ):

        if not documents:
            return []

        pairs = [

            (

                query,

                item["content"],

            )

            for item in documents

        ]

        scores = cls.model().predict(
            pairs
        )

        merged = list(

            zip(
                documents,
                scores,
            )

        )

        merged.sort(

            key=lambda x: x[1],

            reverse=True,

        )

        return [

            item

            for item, _ in merged

        ]