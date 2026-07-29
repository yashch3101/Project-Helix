from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("=" * 80)
    logger.info("Starting Project Helix API...")
    logger.info("=" * 80)

    yield

    logger.info("=" * 80)
    logger.info("Stopping Project Helix API...")
    logger.info("=" * 80)