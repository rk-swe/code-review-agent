import os

from celery import Celery

REDIS_BROKER_URL = os.environ["REDIS_BROKER_URL"]
REDIS_BACKEND_URL = os.environ["REDIS_BACKEND_URL"]


celery_app = Celery(
    "code_review_agent",
    broker=REDIS_BROKER_URL,
    backend=REDIS_BACKEND_URL,
)
celery_app.autodiscover_tasks(["app.tasks"])
