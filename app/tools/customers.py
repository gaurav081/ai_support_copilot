from app.database.database import SessionLocal
from app.database.models import Customer


def get_customer_by_email(email: str) -> dict | None:

    session = SessionLocal()

    try:
        customer = (
            session.query(Customer)
            .filter(
                Customer.email == email
            )
            .first()
        )

        if customer is None:
            return None

        return {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email
        }

    finally:
        session.close()