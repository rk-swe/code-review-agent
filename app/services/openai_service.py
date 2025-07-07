from openai import OpenAI

client = OpenAI()


def test():
    response = client.responses.create(
        model="o4-mini",
        input="Write a one-sentence bedtime story about a unicorn.",
    )
    print(response.output_text)
