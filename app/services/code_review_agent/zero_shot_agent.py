from dataclasses import dataclass

from pydantic_ai import Agent

from app.schemas import pr_analysis_schemas

from .zero_shot_prompts import SYSTEM_PROMPT, USER_PROMPT


@dataclass
class ReviewCodeDeps:
    filename: str
    diff: str
    full_code: str


agent = Agent(
    "openai:o4-mini",
    instructions=SYSTEM_PROMPT,
    deps_type=ReviewCodeDeps,
    output_type=pr_analysis_schemas.PrAnalaysisResultFile,
)


def review_code(
    filename: str, diff: str, full_code: str
) -> pr_analysis_schemas.PrAnalaysisResultFile:
    result = agent.run_sync(
        USER_PROMPT.format(
            filename=filename,
            diff=diff,
            full_code=full_code,
        ),
        deps=ReviewCodeDeps(
            filename=filename,
            diff=diff,
            full_code=full_code,
        ),
    )
    return result.output
