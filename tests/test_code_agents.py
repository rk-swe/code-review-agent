import pytest

from app.handlers.logger import get_logger
from app.services.code_review_agent import zero_shot_agent, zero_shot_llm

logger = get_logger()


@pytest.mark.slow
def test_zero_shot_llm():
    filename = "app/services/pr_analysis_bg_task.py"
    diff = ""
    with open(filename, "r") as fp:
        full_code = fp.read()

    y = zero_shot_llm.review_code(filename, diff, full_code)
    logger.info(y)


@pytest.mark.slow
def test_zero_shot_agent():
    filename = "app/services/pr_analysis_bg_task.py"
    diff = ""
    with open(filename, "r") as fp:
        full_code = fp.read()

    y = zero_shot_agent.review_code(filename, diff, full_code)
    logger.info(y)
