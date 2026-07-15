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

        evidence = EvidenceBuilder.build({

            "retrieval": retrieval,

            "graph": graph,

            "dependency": dependency,

            "context": context,

        })

        impact = ImpactAnalyzer.analyze({

            "graph": graph,

        })

        impact_analysis = []

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

            print("=" * 80)
            print("IMPACT ANALYSIS")
            print(impact_analysis)
            print("=" * 80)

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