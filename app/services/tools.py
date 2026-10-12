
import json

import ollama
from google import genai
from google.genai import types

from app.config import settings
from app.tools.customers import get_customer_by_email
from app.tools.orders import get_order_status
from app.tools.tickets import create_support_ticket


SYSTEM_PROMPT = """
You are a customer support assistant.

Use the available tools when you need customer, order, or
support-ticket information.

Do not invent database information.

Create a support ticket when the customer clearly needs
human assistance.

Treat tool results as the source of truth. Do not invent
fields, values, tracking numbers, dates, carriers, or details
that were not returned by a tool.
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get the current status and details of a customer order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_number": {
                        "type": "string",
                        "description": "The order number, for example ORD1001.",
                    }
                },
                "required": ["order_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_by_email",
            "description": "Find a customer using their email address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The customer's email address.",
                    }
                },
                "required": ["email"],
            },
        },
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
                        "description": "Short title of the support issue.",
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the issue.",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Priority of the support ticket.",
                    },
                    "customer_id": {
                        "type": "integer",
                        "description": "Customer ID if it is known.",
                    },
                },
                "required": ["subject", "description", "priority"],
            },
        },
    },
]


def execute_tool(tool_name: str, arguments: dict) -> dict:
    if tool_name == "get_order_status":
        result = get_order_status(arguments["order_number"])

    elif tool_name == "get_customer_by_email":
        result = get_customer_by_email(arguments["email"])

    elif tool_name == "create_support_ticket":
        result = create_support_ticket(
            subject=arguments["subject"],
            description=arguments["description"],
            priority=arguments["priority"],
            customer_id=arguments.get("customer_id"),
        )

    else:
        raise ValueError(f"Unknown tool: {tool_name}")

    if result is None:
        return {"error": "No matching record was found."}

    return result


def _run_ollama(
    message: str,
    conversation_history: list[dict],
) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *conversation_history,
        {"role": "user", "content": message},
    ]

    response = ollama.chat(
        model=settings.model_name,
        messages=messages,
        tools=TOOLS,
    )

    tool_calls = response["message"].get("tool_calls", [])

    if not tool_calls:
        return response["message"]["content"] or ""

    messages.append(response["message"])

    for tool_call in tool_calls:
        function = tool_call["function"]

        try:
            result = execute_tool(
                function["name"],
                function["arguments"],
            )
        except Exception as exc:
            result = {"error": str(exc)}

        messages.append({
            "role": "tool",
            "content": json.dumps(result),
        })

    final_response = ollama.chat(
        model=settings.model_name,
        messages=messages,
    )

    return final_response["message"]["content"] or ""


def _run_gemini(
    message: str,
    conversation_history: list[dict],
) -> str:
    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY must be configured when using Gemini."
        )

    client = genai.Client(api_key=settings.gemini_api_key)

    declarations = [
        types.FunctionDeclaration(
            name=tool["function"]["name"],
            description=tool["function"]["description"],
            parameters_json_schema=tool["function"]["parameters"],
        )
        for tool in TOOLS
    ]

    gemini_contents = []

    for item in conversation_history:
        role = item.get("role", "user")
        content = item.get("content", "")

        if role == "system" or not content:
            continue

        gemini_role = "model" if role in ("assistant", "model") else "user"

        gemini_contents.append(
            types.Content(
                role=gemini_role,
                parts=[types.Part.from_text(text=str(content))],
            )
        )

    gemini_contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)],
        )
    )

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[types.Tool(function_declarations=declarations)],
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=gemini_contents,
        config=config,
    )

    function_calls = response.function_calls

    if not function_calls:
        return response.text or ""

    # Preserve the model's function-call response for the next turn.
    if not response.candidates:
        raise ValueError("Gemini returned no candidate for its tool call.")

    gemini_contents.append(response.candidates[0].content)

    for function_call in function_calls:
        try:
            result = execute_tool(
                function_call.name,
                dict(function_call.args or {}),
            )
        except Exception as exc:
            result = {"error": str(exc)}

        gemini_contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_function_response(
                        name=function_call.name,
                        response=result,
                    )
                ],
            )
        )

    final_response = client.models.generate_content(
        model=settings.gemini_model,
        contents=gemini_contents,
        config=config,
    )

    return final_response.text or ""


def run_tool_calling(
    message: str,
    conversation_history: list[dict] | None = None,
) -> str:
    conversation_history = conversation_history or []

    provider = settings.llm_provider.lower()

    if provider == "gemini":
        return _run_gemini(message, conversation_history)

    if provider == "ollama":
        return _run_ollama(message, conversation_history)

    raise ValueError(f"Unsupported LLM provider: {provider}")
