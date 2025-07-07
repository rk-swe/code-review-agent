from openai import OpenAI
from schemas import pr_analysis_schemas

client = OpenAI()


def test():
    response = client.responses.create(
        model="o4-mini",
        input="Write a one-sentence bedtime story about a unicorn.",
    )
    print(response.output_text)


def call_code_review(
    filename: str, diff: str, full_code: str
) -> pr_analysis_schemas.PrAnalaysisResultFile:
    system_prompt = """
    You are an expert software engineer and code reviewer. Your job is to analyze code changes and provide constructive feedback across multiple dimensions:

    - Code style and formatting
    - Potential bugs or logical errors
    - Performance optimizations
    - General best practices

    You always return structured, precise, and useful suggestions to improve code quality.
    """

    user_prompt = f"""
    filename:
    {filename}

    diff:
    {diff}

    full_code:
    {full_code}
    """

    response = client.responses.parse(
        model="o4-mini",
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        text_format=pr_analysis_schemas.PrAnalaysisResultFile,
    )
    file_result = response.output_parsed
    return file_result
