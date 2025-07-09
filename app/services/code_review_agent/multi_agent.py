from pydantic_ai import Agent, Tool

from app.handlers.logger import get_logger
from app.schemas import pr_analysis_schemas
from app.services.code_review_agent.common import (
    ReviewCodeDeps,
    only_if_python,
    ruff_linter,
)

from .multi_agent_prompts import (
    BEST_PRACTICE_SYSTEM_PROMPT,
    BUG_AGENT_SYSTEM_PROMPT,
    PERFORMANCE_AGENT_SYSTEM_PROMPT,
    STYLE_AGENT_SYSTEM_PROMPT,
)
from .zero_shot_prompts import USER_PROMPT

logger = get_logger()

style_agent = Agent(
    "openai:o4-mini",
    name="style_agent",
    instructions=STYLE_AGENT_SYSTEM_PROMPT,
    deps_type=ReviewCodeDeps,
    output_type=pr_analysis_schemas.PrAnalaysisResultFile,
)

bug_agent = Agent(
    "openai:o4-mini",
    name="bug_agent",
    instructions=BUG_AGENT_SYSTEM_PROMPT,
    deps_type=ReviewCodeDeps,
    output_type=pr_analysis_schemas.PrAnalaysisResultFile,
    tools=[
        Tool(ruff_linter, takes_ctx=True, prepare=only_if_python),
    ],
)

performance_agent = Agent(
    "openai:o4-mini",
    name="performance_agent",
    instructions=PERFORMANCE_AGENT_SYSTEM_PROMPT,
    deps_type=ReviewCodeDeps,
    output_type=pr_analysis_schemas.PrAnalaysisResultFile,
)

best_practice_agent = Agent(
    "openai:o4-mini",
    name="best_practice_agent",
    instructions=BEST_PRACTICE_SYSTEM_PROMPT,
    deps_type=ReviewCodeDeps,
    output_type=pr_analysis_schemas.PrAnalaysisResultFile,
)


def review_code(
    filename: str, diff: str, full_code: str
) -> pr_analysis_schemas.PrAnalaysisResultFile:
    final_result: list[pr_analysis_schemas.PrAnalaysisResultFile] = []

    for agent in [style_agent, bug_agent, performance_agent, best_practice_agent]:
        logger.info(f"Running agent: {agent.name}")
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
        final_result.append(result.output)

    return pr_analysis_schemas.PrAnalaysisResultFile(
        name=filename,
        issues=[issue for result in final_result for issue in result.issues],
    )
