from openai import OpenAI
from zero_shot_prompts import SYSTEM_PROMPT, USER_PROMPT

from app.schemas import pr_analysis_schemas

client = OpenAI()


def test():
    response = client.responses.create(
        model="o4-mini",
        input="Write a one-sentence bedtime story about a unicorn.",
    )
    print(response.output_text)


def review_code(
    filename: str, diff: str, full_code: str
) -> pr_analysis_schemas.PrAnalaysisResultFile:
    response = client.responses.parse(
        model="o4-mini",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    filename=filename,
                    diff=diff,
                    full_code=full_code,
                ),
            },
        ],
        text_format=pr_analysis_schemas.PrAnalaysisResultFile,
    )
    file_result = response.output_parsed
    return file_result
