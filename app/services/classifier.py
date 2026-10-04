import json
from typing import Literal

import ollama
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
        "other"
    ]

    sentiment: Literal[
        "positive",
        "neutral",
        "negative"
    ]

    priority: Literal[
        "low",
        "medium",
        "high"
    ]


SYSTEM_PROMPT = """
You classify customer support messages.

You MUST return structured data using exactly these values.

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

Choose the single best intent.

Priority should reflect how urgently the support team should handle
the customer's issue.

Do not create new labels.
"""


def analyze_message(
    message: str
) -> MessageAnalysis:

    response = ollama.chat(
        model=settings.model_name,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ],
        format=MessageAnalysis.model_json_schema()
    )

    data = json.loads(
        response["message"]["content"]
    )

    return MessageAnalysis.model_validate(data)