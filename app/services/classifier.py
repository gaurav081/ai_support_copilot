
import json
from typing import Literal

import ollama
from google import genai
from pydantic import BaseModel

from app.config import settings


class MessageAnalysis(BaseModel):
    intent: Literal[
        "return_request",
        "refund_request",
        "shipping_question",
        "order_status",
        "exchange_request",
        "cancellation_request",
        "general_question",
        "other",
    ]

    sentiment: Literal["positive", "neutral", "negative"]

    priority: Literal["low", "medium", "high"]


SYSTEM_PROMPT = """
You classify customer support messages.

Return structured data using exactly these values.

Intent:
- return_request
- refund_request
- shipping_question
- order_status
- exchange_request
- cancellation_request
- general_question
- other

Sentiment:
- positive
- neutral
- negative

Priority:
- low
- medium
- high

Classification rules:
1. Choose the single best intent from the allowed labels.
2. A direct request for human assistance, a human agent,
   a live representative, or escalation must be treated as
   high priority.
3. Examples of direct human-support requests include:
   - "I require human assistance"
   - "I want to talk to a human"
   - "Please connect me to an agent"
   - "I need a real person to help me"
4. For direct human-support requests, use general_question
   as the intent unless another allowed intent is more appropriate.
5. High priority should also be used for urgent issues that
   require prompt support-team attention.
6. Medium priority is for ordinary support issues.
7. Low priority is for non-urgent requests.
8. Sentiment must reflect the customer's expressed emotion.
   Requesting human assistance alone does not necessarily
   mean the customer is negative.
9. Never invent labels or return values outside the
   specified categories.
"""

def analyze_message(message: str) -> MessageAnalysis:
    provider = settings.llm_provider.lower()

    if provider == "gemini":
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY must be configured when using Gemini."
            )

        client = genai.Client(api_key=settings.gemini_api_key)

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=f"Classify this customer support message:\n{message}",
            config={
                "system_instruction": SYSTEM_PROMPT,
                "response_mime_type": "application/json",
                "response_schema": MessageAnalysis,
            },
        )

        if not response.text:
            raise ValueError("Gemini returned an empty classification.")

        return MessageAnalysis.model_validate_json(response.text)

    if provider == "ollama":
        response = ollama.chat(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            format=MessageAnalysis.model_json_schema(),
        )

        data = json.loads(response["message"]["content"])
        return MessageAnalysis.model_validate(data)

    raise ValueError(f"Unsupported LLM provider: {provider}")
