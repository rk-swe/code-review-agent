from app.schemas import pr_analysis_schemas

from . import openai_service


def review_code(
    filename: str, diff: str, full_code: str
) -> pr_analysis_schemas.PrAnalaysisResultFile:
    return openai_service.review_code(filename, diff, full_code)
