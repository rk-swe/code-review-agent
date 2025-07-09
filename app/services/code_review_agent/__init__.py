from app.schemas import pr_analysis_schemas

from . import zero_shot_agent, zero_shot_llm

# TODO: exit non code files fast
# TODO: exit very long files


def review_code(
    filename: str,
    diff: str,
    full_code: str,
    agent_type: pr_analysis_schemas.CodeReviewAgentType = pr_analysis_schemas.CodeReviewAgentType.ZERO_SHOT_LLM,
) -> pr_analysis_schemas.PrAnalaysisResultFile:
    match agent_type:
        case pr_analysis_schemas.CodeReviewAgentType.ZERO_SHOT_LLM:
            return zero_shot_llm.review_code(filename, diff, full_code)

        case pr_analysis_schemas.CodeReviewAgentType.ZERO_SHOT_AGENT:
            return zero_shot_agent.review_code(filename, diff, full_code)

        case _:
            assert False, f"Unknown agent type: {agent_type}"
