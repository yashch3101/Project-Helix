class TokenBudget:

    @staticmethod
    def apply(
        chunks,
        max_chunks=15,
    ):
        """
        Temporary budget manager.

        Later this will become
        token-based instead of chunk-based.
        """

        return chunks[:max_chunks]