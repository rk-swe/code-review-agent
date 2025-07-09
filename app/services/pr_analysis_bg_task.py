from contextlib import contextmanager
from typing import Generator

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from app.handlers.logger import get_logger
from app.models import db_ctx_mgr, models
from app.schemas import pr_analysis_schemas
from app.services import code_review_agent, github_service

logger = get_logger()


# TODO: Can make things concurrent with threads or asyncio

# TODO: Can keep status and error on file also
# and dont stop on one error of file
# complete all files then log error on task


@contextmanager
def task_context(db: Session, task_id: str) -> Generator[None, None, None]:
    db.execute(
        update(models.PrAnalysis)
        .where(models.PrAnalysis.task_id == task_id)
        .values(status=pr_analysis_schemas.TaskStatus.PROCESSING)
    )
    db.commit()
    logger.info(f"Task {task_id}, status = {pr_analysis_schemas.TaskStatus.PROCESSING}")

    try:
        yield
    except Exception as e:
        logger.error("Error occurred", exc_info=True)
        db.rollback()
        db.execute(
            update(models.PrAnalysis)
            .where(models.PrAnalysis.task_id == task_id)
            .values(
                status=pr_analysis_schemas.TaskStatus.FAILED,
                # NOTE: Ideally need to have proper exception hierachy and error handling for now just dumping any error to error field
                error=str(e),
            )
        )
        db.commit()
        logger.info(f"Task {task_id}, status = {pr_analysis_schemas.TaskStatus.FAILED}")
        # raise
    else:
        db.execute(
            update(models.PrAnalysis)
            .where(models.PrAnalysis.task_id == task_id)
            .values(status=pr_analysis_schemas.TaskStatus.COMPLETED)
        )
        db.commit()
        logger.info(
            f"Task {task_id}, status = {pr_analysis_schemas.TaskStatus.COMPLETED}"
        )


def analyze_pr(task_id: str):
    with db_ctx_mgr() as db:
        with task_context(db, task_id):
            analyze_pr_with_db(db, task_id)


def get_analysis_read_data(
    db: Session, task_id: str
) -> pr_analysis_schemas.PrAnalysisReadData:
    db_analysis = db.scalars(
        select(models.PrAnalysis).where(models.PrAnalysis.task_id == task_id)
    ).one()
    return pr_analysis_schemas.PrAnalysisReadData.model_validate(db_analysis)


def analyze_pr_with_db(db: Session, task_id: str):
    logger.info(f"Inside analyze_pr_with_db {task_id}")

    analysis_read_data = get_analysis_read_data(db, task_id)

    pull_request = github_service.get_pull_request(
        analysis_read_data.repo_owner,
        analysis_read_data.repo,
        analysis_read_data.pr_number,
        analysis_read_data.github_token,
    )
    logger.info("Got pull_request")

    diff_entries = github_service.list_pull_request_files(
        analysis_read_data.repo_owner,
        analysis_read_data.repo,
        analysis_read_data.pr_number,
        analysis_read_data.github_token,
    )
    logger.info(f"Got all the diff_entries length = ({len(diff_entries)})")

    for index, diff_entry in enumerate(diff_entries):
        logger.info(f"{index + 1}, {len(diff_entries)}, {diff_entry.filename}")

        diff = github_service.get_patch_from_diff_entry(diff_entry)
        full_code = github_service.get_file_content(
            analysis_read_data.repo_owner,
            analysis_read_data.repo,
            diff_entry.filename,
            pull_request.head.sha,
            analysis_read_data.github_token,
        )
        file_result = code_review_agent.review_code(
            diff_entry.filename, diff, full_code
        )

        db_file = models.PrAnalysisFile(
            task_id=task_id,
            name=diff_entry.filename,
        )
        db.add(db_file)
        db.flush()

        db.execute(
            insert(models.PrAnalysisFileIssue).values(
                [
                    {
                        "file_id": db_file.id,
                        **issue.model_dump(),
                    }
                    for issue in file_result.issues
                ]
            )
        )
        db.commit()
        logger.info(f"{index + 1}, {len(diff_entries)}, {diff_entry.filename}, success")

    logger.info("Completed all diff_entries")
