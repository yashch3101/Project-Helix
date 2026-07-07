from sentence_transformers import SentenceTransformer


class Embedder:

    model = SentenceTransformer(
        "BAAI/bge-base-en-v1.5"
    )

    @classmethod
    def encode(
        cls,
        text: str,
    ):
        return cls.model.encode(
            text,
            normalize_embeddings=True,
        ).tolist()

    @classmethod
    def encode_batch(
        cls,
        texts: list[str],
    ):

        return cls.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=False,
        ).tolist()