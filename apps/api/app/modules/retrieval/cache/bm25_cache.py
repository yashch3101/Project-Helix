from rank_bm25 import BM25Okapi


class BM25Cache:

    _indexes = {}

    @classmethod
    def has(cls, repository_id):

        return repository_id in cls._indexes

    @classmethod
    def get(cls, repository_id):

        return cls._indexes.get(repository_id)

    @classmethod
    def set(

        cls,

        repository_id,

        bm25,

        chunks,

    ):

        cls._indexes[repository_id] = {

            "bm25": bm25,

            "chunks": chunks,

        }

    @classmethod
    def clear(cls, repository_id):

        cls._indexes.pop(repository_id, None)