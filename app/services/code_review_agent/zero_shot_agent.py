from dataclasses import dataclass

from pydantic_ai import Agent

from app.schemas import pr_analysis_schemas

SYSTEM_PROMPT = """
You are an expert software engineer and code reviewer. Your job is to analyze code changes and provide constructive feedback across multiple dimensions:

- Code style and formatting
- Potential bugs or logical errors
- Performance optimizations
- General best practices

You always return structured, precise, and useful suggestions to improve code quality.
"""

USER_PROMPT = """
filename:
{filename}

diff:
{diff}

full_code:
{full_code}
"""


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
