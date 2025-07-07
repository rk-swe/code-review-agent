from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session, joinedload

from app.celery_app import celery_app
from app.handlers.logger import get_logger
from app.models import get_db, models
from app.schemas import pr_analysis_examples, pr_analysis_schemas

logger = get_logger()


router = APIRouter()


# TODO: Add rate limiting
# TODO: Add caching

# NOTE: Could seperate each file to its own child task but unnecessary
# NOTE: For POC, no need for asyncio

# NOTE: Naming could have been better
# For now consider task and analysis as same


####


@router.post(
    "",
    response_model=pr_analysis_schemas.PrAnalysisStatusResponse,
    responses=pr_analysis_examples.CREATE_PR_ANALSYIS_RESPONSE,
)
def create_pr_analysis(
    req_body: pr_analysis_schemas.PrAnalysisCreate, db: Session = Depends(get_db)
) -> pr_analysis_schemas.PrAnalysisStatusResponse:
    # TODO: Reuse previously done work
    # check if (repo_url, pr) already exists in prev task
    # if no create new task
    # if yes check if (repo_url, pr) changed since the task
    # if no just give back prev task_id
    # if yes check each file
    # if file has not changed reuse output else compute output

    db_analysis = models.PrAnalysis(
        **req_body.model_dump(),
        repo=req_body.repo,
        repo_owner=req_body.repo_owner,
        status=pr_analysis_schemas.TaskStatus.PENDING,
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    celery_app.send_task(
        "app.celery_app.process_pr_analysis",
        args=[db_analysis.task_id],
        queue="default",
    )
    logger.info(f"Sent celery_task process_pr_analysis for {db_analysis.task_id}")

    return db_analysis


@router.delete("/", response_model=pr_analysis_schemas.BasicRepsonse)
def delete_all_pr_analysis(db: Session = Depends(get_db)):
    db.execute(delete(models.PrAnalysis))
    db.commit()
    return {"message": "success"}


####


@router.get(
    "/{task_id}/status", response_model=pr_analysis_schemas.PrAnalysisStatusResponse
)
def get_pr_analysis_status(task_id: str, db: Session = Depends(get_db)):
    db_analysis = db.scalars(
        select(models.PrAnalysis).where(models.PrAnalysis.task_id == task_id)
    ).first()
    if not db_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exist"
        )

    return db_analysis


def calculate_summary(db_files: list[models.PrAnalysisFile]) -> dict:
    return {
        "total_files": len(db_files),
        "total_issues": sum(len(db_file.issues) for db_file in db_files),
        "critical_issues": sum(
            sum(1 for db_issue in db_file.issues if db_issue.is_critical)
            for db_file in db_files
        ),
    }


@router.get(
    "/{task_id}/results", response_model=pr_analysis_schemas.PrAnalaysisResultResponse
)
def get_pr_analysis_results(task_id: str, db: Session = Depends(get_db)):
    db_analysis = db.scalars(
        select(models.PrAnalysis)
        .where(models.PrAnalysis.task_id == task_id)
        .options(
            joinedload(models.PrAnalysis.files).joinedload(models.PrAnalysisFile.issues)
        )
    ).first()
    if not db_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exist"
        )

    response_data = {
        "task_id": db_analysis.task_id,
        "repo_url": db_analysis.repo_url,
        "pr_number": db_analysis.pr_number,
        "repo": db_analysis.repo,
        "repo_owner": db_analysis.repo_owner,
        "status": db_analysis.status,
        "error": db_analysis.error,
        "results": {
            "files": db_analysis.files,
            "summary": calculate_summary(db_analysis.files),
        },
    }
    return response_data


@router.delete("/{task_id}", response_model=pr_analysis_schemas.BasicRepsonse)
def delete_pr_analysis(task_id: str, db: Session = Depends(get_db)):
    db.execute(delete(models.PrAnalysis).where(models.PrAnalysis.task_id == task_id))
    db.commit()
    return {"message": "success"}


####
