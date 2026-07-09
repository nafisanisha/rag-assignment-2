from openai import OpenAI

from src.config import (
    OPENAI_API_KEY,
    CHAT_MODEL
)


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def generate_answer(prompt):

    if prompt.strip() == "":
        raise ValueError(
            "Prompt cannot be empty."
        )

    response = client.responses.create(
        model=CHAT_MODEL,
        input=prompt,
        max_output_tokens=200
    )

    final_answer = response.output_text.strip()

    return final_answer