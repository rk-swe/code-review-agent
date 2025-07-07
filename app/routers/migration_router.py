from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import get_db
from app.services import alembic_service

router = APIRouter()


@router.get("/version")
def get_alembic_version(db: Session = Depends(get_db)):
    version_num = db.execute(text("SELECT version_num FROM alembic_version;")).one()[0]
    return {"message": "success", "data": version_num}


@router.post("/upgrade_database")
def upgrade_database(background_tasks: BackgroundTasks):
    background_tasks.add_task(alembic_service.upgrade_database)
    return {"message": "success"}
