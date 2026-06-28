from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Project Helix API...")
    yield
    logger.info("Stopping Project Helix API...")