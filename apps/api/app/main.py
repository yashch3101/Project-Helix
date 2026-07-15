from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from app.core.config import settings
from app.core.lifespan import lifespan
from app.modules.health.router import router as health_router
from app.modules.auth.router import router as auth_router

from app.modules.projects.router import (
    router as project_router,
)

from app.modules.repositories.router import (
    router as repository_router,
)

# from app.modules.scanner.router import (
#     router as scanner_router,
# )

from app.modules.parser.router import (
    router as parser_router,
)

from app.modules.dependency_graph.router import (
    router as dependency_router,
)

from app.modules.code_chunks.router import (
    router as chunk_router,
)

from app.modules.retrieval.router import (
    router as retrieval_router,
)

from app.modules.source_viewer.router import (
    router as source_router,
)

from app.modules.ai.router import router as ai_router

from app.modules.context.router import router as context_router

from app.modules.chat.router import router as chat_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(repository_router)
# app.include_router(scanner_router)
app.include_router(parser_router)
app.include_router(dependency_router)
app.include_router(chunk_router)
app.include_router(retrieval_router)
app.include_router(ai_router)
app.include_router(context_router)
app.include_router(chat_router)
app.include_router(source_router)