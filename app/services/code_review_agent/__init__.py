from app.schemas import pr_analysis_schemas

from . import zero_shot_llm


def review_code(
    filename: str, diff: str, full_code: str
) -> pr_analysis_schemas.PrAnalaysisResultFile:
    return zero_shot_llm.review_code(filename, diff, full_code)
