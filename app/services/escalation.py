def should_escalate(
    priority: str,
    intent: str,
    message: str = ""
) -> bool:
    """Determine whether a customer request needs human support."""

    if priority == "high":
        return True

    message_lower = message.lower()

    human_support_phrases = [
        "human assistance",
        "human support",
        "human agent",
        "talk to a human",
        "speak to a human",
        "talk to an agent",
        "speak to an agent",
        "connect me to an agent",
        "real person",
        "live representative",
        "human representative",
        "escalate to a human",
        "need a person",
    ]

    return any(
        phrase in message_lower
        for phrase in human_support_phrases
    )


def escalate_to_support(
    message: str,
    priority: str,
    customer_id: int | None = None
) -> dict:
    from app.tools.tickets import create_support_ticket

    return create_support_ticket(
        subject="Customer support escalation",
        description=message,
        priority=priority,
        customer_id=customer_id
    )
