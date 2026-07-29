from sentence_transformers import SentenceTransformer


class Embedder:

    model = None

    @classmethod
    def get_model(cls):
        if cls.model is None:
            cls.model = SentenceTransformer(
                "BAAI/bge-base-en-v1.5"
            )
        return cls.model

    @classmethod
    def encode(
        cls,
        text: str,
    ):
        model = cls.get_model()

        return model.encode(
            text,
            normalize_embeddings=True,
        ).tolist()

    @classmethod
    def encode_batch(
        cls,
        texts: list[str],
    ):
        model = cls.get_model()

        return model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=False,
        ).tolist()