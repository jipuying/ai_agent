from fastapi import APIRouter

from app.api.openapi import knowledge

router = APIRouter()
router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"]) 