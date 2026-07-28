from app.modules.ai.agents import RepositoryAgent
from app.modules.ai.context import (
    RepositoryContextBuilder,
    RepositoryContextFormatter,
)
from app.modules.ai.groq_client import GroqClient
from app.modules.ai.intent import IntentAnalyzer
from app.modules.ai.planner import Planner
from app.modules.ai.prompt_builder import PromptBuilder


class RepositoryReasoner:

    @staticmethod
    async def answer(
        db,
        repository_id,
        question: str,
        history: str = "",
    ):

        # 1. Detect intent
        intent = IntentAnalyzer.analyze(question)

        # 2. Build execution plan
        plan = Planner.create_plan(intent)

        # 3. Execute tools
        agent = RepositoryAgent()

        tool_results = await agent.execute(
            db=db,
            repository_id=repository_id,
            query=question,
            plan=plan,
        )

        print("=" * 80)
        print("TOOL RESULTS")
        print(tool_results)
        print("=" * 80)

        # 4. Build context
        context = RepositoryContextBuilder.build(tool_results)

        print("=" * 80)
        print("CONTEXT")
        print(context)
        print("=" * 80)

        # 5. Format context
        formatted_context = (
            RepositoryContextFormatter.format(context)
        )

        # 6. Prompt
        prompt = PromptBuilder.build(
            history=history,
            context=formatted_context,
            question=question,
        )

        # 7. LLM
        answer = await GroqClient.generate(prompt)

        return answer