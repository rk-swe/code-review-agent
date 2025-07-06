from fastapi import APIRouter

from app.routers import pr_analysis_router

router = APIRouter()

router.include_router(
    pr_analysis_router.router,
    prefix="/pr-analysis",
    tags=["PR Analysis"],
)
