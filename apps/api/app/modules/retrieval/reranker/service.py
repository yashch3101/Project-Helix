from sentence_transformers import CrossEncoder
from typing import Any

VECTOR_SCORE_WEIGHT = 0.25

FUNCTION_BOOST = 0.15

MIN_RERANK_SCORE = 0.35

FALLBACK_RESULTS = 5

MODEL_NAME = (
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


class RerankerService:

    _model: CrossEncoder | None = None

    @classmethod
    def model(cls):

        if cls._model is None:

            cls._model = CrossEncoder(
                MODEL_NAME
            )

        return cls._model

    @classmethod
    def rerank(
        cls,
        query: str,
        documents: list[dict[str, Any]],
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

        boosted = []

        for item, score in zip(documents, scores):

            final_score = float(score)

            # Vector similarity bonus
            final_score += (
                item.get("score", 0)
                * VECTOR_SCORE_WEIGHT
            )

            chunk_type = item.get("chunk_type", "")

            if chunk_type in {
                "function",
                "method",
                "class",
            }:
                final_score += FUNCTION_BOOST

            boosted.append(
                (
                    item,
                    final_score,
                )
            )

        boosted.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        filtered = []

        for item, score in boosted:

            if score >= MIN_RERANK_SCORE:
                filtered.append(
                    (
                        item,
                        score,
                    )
                )

        filtered.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        if not filtered:
            return [
                item
                for item, _ in boosted[:FALLBACK_RESULTS]
            ]

        return [
            item
            for item, _ in filtered
        ]