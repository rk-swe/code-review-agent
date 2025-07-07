from .celery_app import celery_app


@celery_app.task
def process_pr_analysis(task_id: str):
    print(f"Starting celery task process_pr_analysis for {task_id}")
    print(f"Completed PR analysis for {task_id}")
    return {"status": "completed", "task_id": task_id}
