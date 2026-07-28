from rank_bm25 import BM25Okapi

from app.modules.retrieval.tokenizer import Tokenizer


class BM25Index:

    @staticmethod
    def build(chunks):

        if not chunks:
            return None

        corpus = []

        for chunk in chunks:

            tokens = Tokenizer.tokenize(chunk.content)

            if tokens:
                corpus.append(tokens)

        if not corpus:
            return None

        return BM25Okapi(corpus)