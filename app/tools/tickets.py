from app.database.database import SessionLocal
from app.database.models import SupportTicket


def create_support_ticket(
    subject: str,
    description: str,
    priority: str,
    customer_id: int | None = None
) -> dict:

    session = SessionLocal()

    try:

        ticket = SupportTicket(
            customer_id=customer_id,
            subject=subject,
            description=description,
            priority=priority,
            status="open"
        )

        session.add(ticket)
        session.commit()
        session.refresh(ticket)

        return {
            "ticket_id": ticket.id,
            "subject": ticket.subject,
            "priority": ticket.priority,
            "status": ticket.status
        }

    finally:
        session.close()