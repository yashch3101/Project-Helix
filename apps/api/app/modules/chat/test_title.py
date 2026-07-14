import asyncio

from app.modules.chat.title_service import TitleService


async def main():

    title = await TitleService.generate(
        "How does APIRouter work in FastAPI?"
    )

    print(title)


asyncio.run(main())