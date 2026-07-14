from rank_bm25 import BM25Okapi

from app.modules.retrieval.tokenizer import Tokenizer


class BM25Index:

    @staticmethod
    def build(chunks):

        corpus = [

            Tokenizer.tokenize(

                chunk.content

            )

            for chunk in chunks

        ]

        return BM25Okapi(corpus)