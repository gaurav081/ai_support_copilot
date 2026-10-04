from app.tools.customers import get_customer_by_email


result = get_customer_by_email(
    "aarav@example.com"
)

print("\nCustomer information:")
print(result)