from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    return {
        "message": "Welcome to Project Helix API"
    }

@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Project Helix API",
        "version": "1.0.0"
    }