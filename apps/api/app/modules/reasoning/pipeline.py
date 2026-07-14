from app.modules.retrieval.service import RetrievalService
from app.modules.graph_retrieval.service import GraphRetrievalService
from app.modules.dependency_expansion.service import (
    DependencyExpansionService,
)

from app.modules.context_compression.service import (
    ContextCompressionService,
)

from app.modules.reasoning.trace_builder import (
    TraceBuilder,
)

from app.modules.context.service import ContextService


class ReasoningPipeline:

    @staticmethod
    async def run(
        db,
        repository_id,
        query,
        top_k=10,
    ):

        # Step 1
        retrieval = await RetrievalService.search(
            db=db,
            repository_id=repository_id,
            query=query,
            top_k=top_k,
        )

        # Step 2
        graph = await GraphRetrievalService.expand(
            db=db,
            repository_id=repository_id,
            symbols=[
                item["chunk_name"]
                if isinstance(item, dict)
                else item.chunk_name
                for item in retrieval
            ],
        )

        # Step 3
        dependency = await DependencyExpansionService.expand(
            db=db,
            repository_id=repository_id,
            retrieval_results=retrieval,
        )

        # Step 4
        context = await ContextService.build(
            db=db,
            repository_id=repository_id,
            query=query,
            top_k=10,
        )

        context = ContextCompressionService.compress(
            context
        )

        print("=" * 80)
        print("COMPRESSED CONTEXT:", len(context))
        print("=" * 80)

        trace = TraceBuilder.build({

            "retrieval": retrieval,

            "graph": graph,

            "dependency": dependency,

            "context": context,

        })

        return {

            "retrieval": retrieval,

            "graph": graph,

            "dependency": dependency,

            "context": context,

            "trace": trace,

        }