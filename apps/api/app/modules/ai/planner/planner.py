from app.modules.ai.intent import IntentResult, IntentType

from .models import (
    AgentType,
    ExecutionPlan,
    ToolType,
)


class Planner:

    @staticmethod
    def create_plan(
        intent: IntentResult,
    ) -> ExecutionPlan:

        # Repository / Explain Queries
        if intent.intent in (
            IntentType.EXPLAIN,
            IntentType.FUNCTION,
            IntentType.CLASS,
            IntentType.FILE,
            IntentType.SEARCH,
            IntentType.GENERAL,
        ):

            return ExecutionPlan(
                agent=AgentType.REPOSITORY,
                tools=[
                    ToolType.VECTOR_SEARCH,
                    ToolType.GRAPH_SEARCH,
                    ToolType.DEPENDENCY_SEARCH,
                ],
                intent=intent.intent.value,
                entity=intent.entity,
            )

        # Architecture
        if intent.intent == IntentType.ARCHITECTURE:

            return ExecutionPlan(
                agent=AgentType.REPOSITORY,
                tools=[
                    ToolType.SUMMARY,
                    ToolType.GRAPH_SEARCH,
                ],
                intent=intent.intent.value,
                entity=intent.entity,
            )

        # Documentation
        if intent.intent == IntentType.DOCUMENTATION:

            return ExecutionPlan(
                agent=AgentType.DOCUMENTATION,
                tools=[
                    ToolType.SUMMARY,
                    ToolType.GRAPH_SEARCH,
                ],
                intent=intent.intent.value,
                entity=intent.entity,
            )

        # Review
        if intent.intent == IntentType.REVIEW:

            return ExecutionPlan(
                agent=AgentType.REVIEW,
                tools=[
                    ToolType.CODE_REVIEW,
                    ToolType.DEPENDENCY_SEARCH,
                ],
                intent=intent.intent.value,
                entity=intent.entity,
            )

        # Bug
        if intent.intent == IntentType.BUG:

            return ExecutionPlan(
                agent=AgentType.BUG,
                tools=[
                    ToolType.BUG_ANALYSIS,
                    ToolType.DEPENDENCY_SEARCH,
                ],
                intent=intent.intent.value,
                entity=intent.entity,
            )

        # Refactor
        if intent.intent == IntentType.REFACTOR:

            return ExecutionPlan(
                agent=AgentType.REFACTOR,
                tools=[
                    ToolType.CODE_REVIEW,
                    ToolType.DEPENDENCY_SEARCH,
                ],
                intent=intent.intent.value,
                entity=intent.entity,
            )

        # Default
        return ExecutionPlan(
            agent=AgentType.REPOSITORY,
            tools=[
                ToolType.VECTOR_SEARCH,
            ],
            intent=intent.intent.value,
            entity=intent.entity,
        )