from app.database.database import Base, SessionLocal, engine
from app.database.models import Customer, Order


def seed_database():

    Base.metadata.create_all(
        bind=engine
    )

    session = SessionLocal()

    try:
        existing_customers = session.query(Customer).count()

        if existing_customers > 0:
            print("Database already contains data.")
            return

        customers = [
            Customer(
                name="Aarav Sharma",
                email="aarav@example.com"
            ),
            Customer(
                name="Priya Verma",
                email="priya@example.com"
            ),
            Customer(
                name="Rahul Mehta",
                email="rahul@example.com"
            )
        ]

        session.add_all(customers)
        session.commit()

        orders = [
            Order(
                order_number="ORD1001",
                customer_id=customers[0].id,
                status="shipped",
                total_amount=1499.00
            ),
            Order(
                order_number="ORD1002",
                customer_id=customers[0].id,
                status="delivered",
                total_amount=2499.00
            ),
            Order(
                order_number="ORD1003",
                customer_id=customers[1].id,
                status="processing",
                total_amount=999.00
            ),
            Order(
                order_number="ORD1004",
                customer_id=customers[2].id,
                status="cancelled",
                total_amount=1799.00
            )
        ]

        session.add_all(orders)
        session.commit()

        print("Database seeded successfully.")

    finally:
        session.close()


if __name__ == "__main__":
    seed_database()