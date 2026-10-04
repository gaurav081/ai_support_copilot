import ollama

from app.config import settings


SYSTEM_PROMPT = """
You are an AI customer support assistant.

Answer the customer's question using the provided knowledge base context.

Important rules:

1. Use information from the knowledge base as the primary source of truth.

2. Identify which parts of the knowledge base are relevant to the
   customer's question and use those parts.

3. You may paraphrase and combine information that is explicitly stated
   in the knowledge base.

4. Do not invent information that is not supported by the knowledge base.

5. Do not invent:
   - buttons
   - URLs
   - policies
   - prices
   - deadlines
   - requirements
   - procedural steps
   - order details

6. If the knowledge base contains partial information, provide the
   information that is supported and clearly state what is not specified.

7. Do not say that information is unavailable when the knowledge base
   explicitly provides an answer.

8. Conversation history may help understand references to previous
   messages, but conversation history is not a source of company policy.

9. Keep the answer concise and directly answer the customer's question.
"""


def generate_response(
    prompt: str,
    context: str,
    conversation_history: list[dict] | None = None
) -> str:

    conversation_history = (
        conversation_history
        if conversation_history is not None
        else []
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(
        conversation_history
    )

    messages.append(
        {
            "role": "user",
            "content": f"""
Knowledge base context:

{context}

Customer question:

{prompt}

Answer the customer using the relevant information from the
knowledge base context.
"""
        }
    )

    response = ollama.chat(
        model=settings.model_name,
        messages=messages
    )

    return response["message"]["content"]