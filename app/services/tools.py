
import json

import ollama

from app.config import settings
from app.tools.customers import get_customer_by_email
from app.tools.orders import get_order_status
from app.tools.tickets import create_support_ticket


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": (
                "Get the current status and details of a customer order."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_number": {
                        "type": "string",
                        "description": (
                            "The order number, for example ORD1001."
                        )
                    }
                },
                "required": ["order_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_by_email",
            "description": (
                "Find a customer using their email address."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": (
                            "The customer's email address."
                        )
                    }
                },
                "required": ["email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_support_ticket",
            "description": (
                "Create a support ticket when a customer issue "
                "needs human assistance."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Short title of the support issue."
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the issue."
                    },
                    "priority": {
                        "type": "string",
                        "enum": [
                            "low",
                            "medium",
                            "high"
                        ],
                        "description": "Priority of the support ticket."
                    },
                    "customer_id": {
                        "type": "integer",
                        "description": (
                            "Customer ID if it is known."
                        )
                    }
                },
                "required": [
                    "subject",
                    "description",
                    "priority"
                ]
            }
        }
    }
]


def execute_tool(
    tool_name: str,
    arguments: dict
) -> dict:

    if tool_name == "get_order_status":

        result = get_order_status(
            arguments["order_number"]
        )

    elif tool_name == "get_customer_by_email":

        result = get_customer_by_email(
            arguments["email"]
        )

    elif tool_name == "create_support_ticket":

        result = create_support_ticket(
            subject=arguments["subject"],
            description=arguments["description"],
            priority=arguments["priority"],
            customer_id=arguments.get("customer_id")
        )

    else:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    if result is None:
        return {
            "error": "No matching record was found."
        }

    return result


def run_tool_calling(
    message: str,
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
            "content": (
                "You are a customer support assistant. "
                "Use the available tools when you need "
                "customer, order, or support-ticket information. "
                "Do not invent database information. "
                "Create a support ticket when the customer "
                "clearly needs human assistance. "
                "When a tool returns data, treat that data as "
                "the only source of truth for the tool-related "
                "answer. Do not add fields, values, tracking "
                "numbers, dates, carriers, or other details "
                "that were not returned by the tool."
            )
        }
    ]

    messages.extend(
        conversation_history
    )

    messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    response = ollama.chat(
        model=settings.model_name,
        messages=messages,
        tools=TOOLS
    )

    tool_calls = response["message"].get(
        "tool_calls",
        []
    )

    if not tool_calls:
        return response["message"]["content"]

    messages.append(
        response["message"]
    )

    for tool_call in tool_calls:

        function = tool_call["function"]

        tool_name = function["name"]
        arguments = function["arguments"]

        result = execute_tool(
            tool_name,
            arguments
        )

        messages.append(
            {
                "role": "tool",
                "content": json.dumps(result)
            }
        )

    final_response = ollama.chat(
        model=settings.model_name,
        messages=messages
    )

    return final_response["message"]["content"]
