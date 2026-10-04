from app.services.tools import run_tool_calling


questions = [
    "What is the status of order ORD1001?",
    "What is the status of order ORD1003?"
]


for question in questions:

    print(f"\nCustomer: {question}")

    answer = run_tool_calling(
        question
    )

    print(f"Assistant: {answer}")