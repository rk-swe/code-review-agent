fastapi dev

celery -A app.celery_app.celery_app worker --loglevel=info --queues=default
