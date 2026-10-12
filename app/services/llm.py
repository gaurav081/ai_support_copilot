
import ollama
from google import genai

from app.config import settings


SYSTEM_PROMPT = """
You are an AI customer support assistant.

Answer the customer's question using the provided knowledge base context.

Important rules:

1. Use information from the knowledge base as the primary source of truth.
2. Use relevant information explicitly supported by the knowledge base.
3. You may paraphrase and combine supported information.
4. Do not invent information, buttons, URLs, policies, prices,
   deadlines, requirements, procedural steps, or order details.
5. If information is partial, explain what is supported and what
   is not specified.
6. Do not claim information is unavailable when the knowledge base
   explicitly provides an answer.
7. Conversation history helps resolve references but is not a source
   of company policy.
8. Keep the answer concise and directly answer the question.
"""


def generate_response(
    prompt: str,
    context: str,
    conversation_history: list[dict] | None = None,
) -> str:
    conversation_history = conversation_history or []

    user_prompt = f"""
Knowledge base context:

{context}

Customer question:

{prompt}

Answer the customer using the relevant information from the
knowledge base context.
"""

    provider = settings.llm_provider.lower()

    if provider == "gemini":
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY must be configured when using Gemini."
            )

        client = genai.Client(api_key=settings.gemini_api_key)

        history = []
        for message in conversation_history:
            role = message.get("role", "user")
            content = message.get("content", "")

            # Gemini conversation roles are "user" and "model".
            if role == "assistant":
                role = "model"
            elif role != "model":
                role = "user"

            history.append(f"{role.upper()}: {content}")

        full_prompt = "\n\n".join(history + [user_prompt])

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=full_prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
            },
        )

        return response.text or ""

    if provider == "ollama":
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history,
            {"role": "user", "content": user_prompt},
        ]

        response = ollama.chat(
            model=settings.model_name,
            messages=messages,
        )

        return response["message"]["content"]

    raise ValueError(f"Unsupported LLM provider: {provider}")
