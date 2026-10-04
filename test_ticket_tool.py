from app.tools.tickets import create_support_ticket


result = create_support_ticket(
    subject="Damaged order",
    description="Customer reported that the order arrived damaged.",
    priority="high",
    customer_id=1
)

print("\nCreated ticket:")
print(result)