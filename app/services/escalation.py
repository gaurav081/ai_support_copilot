def should_escalate(
    priority: str,
    intent: str
) -> bool:

    if priority != "high":
        return False

    escalation_intents = {
        "other"
    }

    return intent in escalation_intents


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