from .rewriter import QueryRewriter


class QueryRewriterService:

    @staticmethod
    def rewrite(query):

        return QueryRewriter.rewrite(query)