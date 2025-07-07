from alembic import command
from alembic.config import Config
from app.handlers.logger import get_logger
from app.models import DB_URL


def upgrade_database():
    logger = get_logger()
    logger.info("Running Alembic migrations...")
    print("Running Alembic migrations...")

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", DB_URL)
    command.upgrade(alembic_cfg, "head")

    logger.info("Alembic Migrations complete.")
    print("Alembic Migrations complete.")
