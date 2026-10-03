import ollama

from app.config import settings


SYSTEM_PROMPT = """
You are an AI customer support assistant.

Your job is to:
- Help customers with their questions.
- Be clear, polite, and concise.
- If you do not know something, say that you do not have enough information.
- Do not invent company policies, prices, order details, or other facts.
"""


def generate_response(prompt: str) -> str:
    response = ollama.chat(
        model=settings.model_name,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]