import asyncio

from app.db.session import AsyncSessionLocal
from app.modules.ai.reasoner import RepositoryReasoner


async def main():

    repository_id = input("Repository ID: ")
    question = input("Question: ")

    async with AsyncSessionLocal() as db:

        answer = await RepositoryReasoner.answer(
            db=db,
            repository_id=repository_id,
            question=question,
        )

    print("\n")
    print("=" * 80)
    print("AI ANSWER")
    print("=" * 80)
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())