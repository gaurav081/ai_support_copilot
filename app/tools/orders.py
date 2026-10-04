from app.database.database import SessionLocal
from app.database.models import Order


def get_order_status(order_number: str) -> dict | None:

    session = SessionLocal()

    try:
        order = (
            session.query(Order)
            .filter(
                Order.order_number == order_number
            )
            .first()
        )

        if order is None:
            return None

        return {
            "order_number": order.order_number,
            "status": order.status,
            "total_amount": order.total_amount,
            "customer_id": order.customer_id
        }

    finally:
        session.close()