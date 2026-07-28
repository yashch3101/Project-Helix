from app.modules.ai.planner import ExecutionPlan
from app.modules.ai.tools import ToolRegistry


class RepositoryAgent:

    async def execute(
        self,
        db,
        repository_id,
        query: str,
        plan: ExecutionPlan,
    ):

        results = []

        for tool in plan.tools:

            tool_instance = ToolRegistry.get(tool.value)

            if tool_instance is None:
                continue

            result = await tool_instance.execute(
                db=db,
                repository_id=repository_id,
                query=query,
                plan=plan,
            )

            results.append(result)

        return results