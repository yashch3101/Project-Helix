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

from app.modules.reasoning.evidence_builder import (
    EvidenceBuilder,
)

from app.modules.reasoning.impact import (
    ImpactAnalyzer,
)

from app.modules.impact.service import ImpactService

from app.modules.context.service import ContextService

from app.modules.reasoning.intent import IntentClassifier

from app.modules.query_rewriter.service import (
    QueryRewriterService,
)

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


class ReasoningPipeline:

    @staticmethod
    async def run(
        db: AsyncSession,
        repository_id: UUID,
        query: str,
        top_k: int = 5,
    ):

        plan = IntentClassifier.classify(query)

        rewrite = QueryRewriterService.rewrite(query)

        # Step 1
        retrieval = await RetrievalService.search(
            db=db,
            repository_id=repository_id,
            query=rewrite.rewritten,
            top_k=min(
                top_k,
                plan.retrieval_limit,
            )
        )

        # Step 2
        graph = []

        if plan.expand_graph:

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
        dependency = []

        if plan.expand_dependencies:

            dependency = await DependencyExpansionService.expand(
                db=db,
                repository_id=repository_id,
                retrieval_results=retrieval,
            )

        # Step 4
        context = []

        if plan.use_context:

            context = await ContextService.build(
                db=db,
                retrieval_results=retrieval,
            )

            context = ContextCompressionService.compress(
                context
            )

        reasoning_data = {

            "retrieval": retrieval,

            "graph": graph,

            "dependency": dependency,

            "context": context,

        }

        trace = TraceBuilder.build(
            reasoning_data
        )

        evidence = EvidenceBuilder.build(
            reasoning_data
        )

        impact = ImpactAnalyzer.analyze(
            {
                "graph": graph,
            }
        )

        impact_analysis = []

        if plan.use_impact:

            processed = set()

            for edge in graph:

                if edge.source_symbol in processed:
                    continue

                processed.add(edge.source_symbol)

                result = await ImpactService.analyze(
                    db=db,
                    repository_id=repository_id,
                    symbol=edge.source_symbol,
                )

                impact_analysis.append(result)

        return {

            "retrieval": retrieval,

            "graph": graph,

            "dependency": dependency,

            "context": context,

            "trace": trace,

            "evidence": evidence,

            "impact": impact,

            "impact_analysis": impact_analysis,

        }