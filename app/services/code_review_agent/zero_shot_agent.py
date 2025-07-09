from pydantic_ai import Agent, RunContext, Tool

from app.schemas import pr_analysis_schemas
from app.services.code_review_agent.common import (
    ReviewCodeDeps,
    only_if_python,
    ruff_linter,
)

from .zero_shot_prompts import LANGUAGE_PROMPTS, SYSTEM_PROMPT, USER_PROMPT

agent = Agent(
    "openai:o4-mini",
    instructions=SYSTEM_PROMPT,
    deps_type=ReviewCodeDeps,
    output_type=pr_analysis_schemas.PrAnalaysisResultFile,
    tools=[
        Tool(ruff_linter, takes_ctx=True, prepare=only_if_python),
    ],
)


@agent.instructions
def add_language_specific_prompts(ctx: RunContext[ReviewCodeDeps]) -> str:
    if ctx.deps.filename.endswith(".py"):
        return LANGUAGE_PROMPTS[".py"]
    elif ctx.deps.filename.endswith(".js"):
        return LANGUAGE_PROMPTS[".js"]

    return ""


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
