from app.modules.repository_summary.analyzer import RepositoryAnalyzer
from app.modules.repository_summary.builder import RepositorySummaryBuilder
from app.modules.repository_summary.intelligence.architecture_generator import (
    ArchitectureGenerator,
)
from app.modules.repository_summary.intelligence.execution_flow_generator import (
    ExecutionFlowGenerator,
)
from app.modules.repository_summary.intelligence.module_explainer import (
    ModuleExplainer,
)
from app.modules.repository_summary.intelligence.dependency_analyzer import (
    DependencyAnalyzer,
)
from app.modules.repository_summary.intelligence.repository_reasoner import (
    RepositoryReasoner,
)
from app.modules.repository_summary.intelligence.architecture_reasoner import (
    ArchitectureReasoner,
)
from app.modules.repository_summary.models import RepositorySummary
from app.modules.repository_summary.repository import RepositorySummaryRepository
from app.modules.repository_index.models import RepositoryFile
from sqlalchemy import select


class RepositorySummaryService:

    @staticmethod
    async def test(
        db,
        repository_id,
    ):

        summary = await RepositoryAnalyzer.analyze(
            db=db,
            repository_id=repository_id,
        )

        files = (
            await db.execute(
                select(RepositoryFile).where(
                    RepositoryFile.repository_id == repository_id
                )
            )
        ).scalars().all()

        knowledge_card = RepositorySummaryBuilder.build(
            summary
        )

        execution_flow = ExecutionFlowGenerator.generate(
            summary
        )

        architecture = ArchitectureGenerator.generate(
            summary
        )

        dependencies = await DependencyAnalyzer.analyze(
            db,
            repository_id,
        )

        module_summary = ModuleExplainer.generate(
            files
        )

        repository_reasoning = RepositoryReasoner.generate(
            summary,
            module_summary,
            dependencies,
        )

        architecture_reasoning = ArchitectureReasoner.generate(
            summary,
            module_summary,
            dependencies,
        )

        repository_summary = RepositorySummary(

        repository_id=repository_id,

        language=summary["language"],

        framework=summary["framework"],

        repository_type=summary["repository_type"],

        entry_points="\n".join(
            summary["entry_points"]
        ),

        api_routes="\n".join(
            summary["api_routes"]
        ),

        total_files=summary["total_files"],

        total_classes=summary["total_classes"],

        total_functions=summary["total_functions"],

        total_modules=summary["total_modules"],

        important_modules="\n".join(
            summary["important_modules"]
        ),

        architecture=architecture,

        execution_flow=execution_flow,

        knowledge_card=knowledge_card,
    )

        await RepositorySummaryRepository.save_or_update(

            db,

            repository_summary,

        )

        print("=" * 80)
        print("SUMMARY SAVED")
        print("=" * 80)

        print("=" * 80)
        print("MODULE EXPLAINER")
        print("=" * 80)

        for module in module_summary:

            print(module["module"])

            for responsibility in module["responsibilities"]:

                print("  -", responsibility)

        print("=" * 80)
        print("DEPENDENCY ANALYZER")
        print("=" * 80)

        if not dependencies:

            print("No graph dependencies found.")

        else:

            for source, targets in dependencies.items():

                print(source)

                for target in sorted(targets):

                    print("   ↓")

                    print("   ", target)

                print()

        print("=" * 80)
        print("REPOSITORY REASONER")
        print("=" * 80)

        print(repository_reasoning)

        print("=" * 80)
        print("ARCHITECTURE REASONER")
        print("=" * 80)

        print(
            architecture_reasoning
        )

        return {

            "summary": summary,

            "knowledge_card": knowledge_card,

            "architecture": architecture,

            "execution_flow": execution_flow,

            "modules": module_summary,

            "dependencies": dependencies,

            "reasoning": repository_reasoning,

            "architecture_reasoning": architecture_reasoning,

        }