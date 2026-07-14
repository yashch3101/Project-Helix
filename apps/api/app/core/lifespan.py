from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from app.core.logger import logger
from app.db.session import AsyncSessionLocal

from app.modules.repositories.models import Repository
from app.modules.indexing.service import IndexingService


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting Project Helix API...")

    logger.info("=" * 80)
    logger.info("BM25 CACHE WARMUP STARTED")
    logger.info("=" * 80)

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Repository)
        )

        repositories = result.scalars().all()

        for repository in repositories:

            try:

                logger.info(
                    f"Loading BM25 -> {repository.name}"
                )

                await IndexingService.rebuild(
                    db=db,
                    repository_id=repository.id,
                )

            except Exception as e:

                logger.error(
                    f"Failed -> {repository.name}"
                )

                logger.error(str(e))

    logger.info("=" * 80)
    logger.info("BM25 CACHE READY")
    logger.info("=" * 80)

    yield

    logger.info("Stopping Project Helix API...")