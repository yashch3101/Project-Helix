import asyncio

from app.db.session import AsyncSessionLocal
from app.modules.ai.agents import RepositoryAgent
from app.modules.ai.context import (
    RepositoryContextBuilder,
    RepositoryContextFormatter,
)
from app.modules.ai.intent import IntentAnalyzer
from app.modules.ai.planner import Planner


async def main():

    repository_id = input("Repository ID: ")
    query = input("Question: ")

    intent = IntentAnalyzer.analyze(query)
    plan = Planner.create_plan(intent)

    async with AsyncSessionLocal() as db:

        agent = RepositoryAgent()

        results = await agent.execute(
            db=db,
            repository_id=repository_id,
            query=query,
            plan=plan,
        )

    context = RepositoryContextBuilder.build(results)

    formatted = RepositoryContextFormatter.format(context)

    print("\n")
    print("=" * 80)
    print("REPOSITORY CONTEXT")
    print("=" * 80)
    print(formatted)


if __name__ == "__main__":
    asyncio.run(main())