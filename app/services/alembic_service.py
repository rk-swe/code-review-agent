from alembic import command
from alembic.config import Config
from app.models import DB_URL


def upgrade_database():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", DB_URL)
    command.upgrade(alembic_cfg, "head")
