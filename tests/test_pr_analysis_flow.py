import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models import get_db, models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)
    os.remove("./test.db")


def test_pr_analysis_full_flow():
    url_prefix = "/api/v1/pr-analysis"

    # Step 1: Create
    create_resp = client.post(
        f"{url_prefix}",
        json={
            "repo_url": "https://github.com/rk-swe/code-review-agent",
            "pr_number": 1,
            "github_token": "fake-token",
        },
    )
    assert create_resp.status_code == 200
    create_data = create_resp.json()
    task_id = create_data["task_id"]

    # Step 2: Get Status
    status_resp = client.get(f"{url_prefix}/{task_id}/status")
    assert status_resp.status_code == 200

    # Step 3: Get Results
    result_resp = client.get(f"{url_prefix}/{task_id}/results")
    assert result_resp.status_code == 200

    # Step 4: Delete
    delete_resp = client.delete(f"{url_prefix}/{task_id}")
    assert delete_resp.status_code == 200
