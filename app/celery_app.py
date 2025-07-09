from dotenv import load_dotenv

load_dotenv()


import os  # noqa: E402

from celery import Celery  # noqa: E402

from app.handlers.logger import get_logger  # noqa: E402
from app.services import pr_analysis_bg_task  # noqa: E402

REDIS_BROKER_URL = os.environ["REDIS_BROKER_URL"]
REDIS_BACKEND_URL = os.environ["REDIS_BACKEND_URL"]


logger = get_logger()


celery_app = Celery(
    "code_review_agent",
    broker=REDIS_BROKER_URL,
    backend=REDIS_BACKEND_URL,
)


@celery_app.task
def process_pr_analysis(task_id: str):
    logger.info(f"Starting celery_task process_pr_analysis for {task_id}")
    pr_analysis_bg_task.analyze_pr(task_id)
    logger.info(f"Completed celery_task process_pr_analysis for {task_id}")
    return {"status": "completed", "task_id": task_id}
