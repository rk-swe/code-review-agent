from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import get_db
from app.schemas.pr_analysis_schemas import PrAnalysisCreate

router = APIRouter()


@router.post("")
def create_pr_analysis(req_body: PrAnalysisCreate, db: Session = Depends(get_db)):
    return {"message": "success", "data": {}}


@router.post("/{task_id}/status")
def get_analyze_pr_task_status(task_id: UUID, db: Session = Depends(get_db)):
    return {"message": "success", "data": {}}


@router.post("/{task_id}/results")
def get_analyze_pr_task_results(task_id: UUID, db: Session = Depends(get_db)):
    return {"message": "success", "data": {}}
