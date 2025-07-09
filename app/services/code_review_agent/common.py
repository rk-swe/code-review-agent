import subprocess
from dataclasses import dataclass

from pydantic_ai import RunContext
from pydantic_ai.tools import ToolDefinition

from app.handlers.logger import get_logger

logger = get_logger()


@dataclass
class ReviewCodeDeps:
    filename: str
    diff: str
    full_code: str


async def only_if_python(
    ctx: RunContext[ReviewCodeDeps], tool_def: ToolDefinition
) -> ToolDefinition | None:
    if ctx.deps.filename.endswith(".py"):
        return tool_def


def ruff_linter(ctx: RunContext[ReviewCodeDeps]) -> str:
    """
    This tool uses Ruff to analyze Python code for linting issues.
    The code is provided through the `RunContext` as part of the `ReviewCodeDeps` dataclass.

    Returns:
        str: The Ruff linting output. If there are linting issues, returns Ruff's formatted output.
             If Ruff encounters internal errors, returns both stdout and stderr.
             If no issues are found, Ruff's standard output.
    """
    logger.info("Running Ruff linter on the provided code...")

    result = subprocess.run(
        ["ruff", "check", "--stdin-filename", ctx.deps.filename, "-"],
        input=ctx.deps.full_code.encode("utf-8"),
        capture_output=True,
        check=False,
    )
    output = result.stdout.decode("utf-8").strip()
    error_output = result.stderr.decode("utf-8").strip()

    if result.returncode != 0 and error_output:
        logger.error(output)
        logger.error(error_output)
        return "Ruff linter encountered an error"

    logger.info("Ruff linter completed successfully.")
    return output
