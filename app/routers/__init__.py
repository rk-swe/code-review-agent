from fastapi import APIRouter

from app.routers import migration_router, pr_analysis_router

router = APIRouter()

router.include_router(
    pr_analysis_router.router,
    prefix="/pr-analysis",
    tags=["PR Analysis"],
)
router.include_router(
    migration_router.router,
    prefix="/migration",
    tags=["Migration"],
)
