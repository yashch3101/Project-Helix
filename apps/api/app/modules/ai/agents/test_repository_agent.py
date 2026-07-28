import asyncio

from app.db.session import AsyncSessionLocal

from app.modules.ai.intent import IntentAnalyzer
from app.modules.ai.planner import Planner
from app.modules.ai.agents import RepositoryAgent


async def main():

    repository_id = input("Repository ID: ")
    question = input("Question: ")

    agent = RepositoryAgent()

    intent = IntentAnalyzer.analyze(question)

    print("\nIntent:")
    print(intent)

    plan = Planner.create_plan(intent)

    print("\nExecution Plan:")
    print(plan)

    async with AsyncSessionLocal() as db:

        results = await agent.execute(
            db=db,
            repository_id=repository_id,
            query=question,
            plan=plan,
        )

    print("\n" + "=" * 80)
    print("AGENT RESULTS")
    print("=" * 80)

    for r in results:
        print()
        print(r)


if __name__ == "__main__":
    asyncio.run(main())