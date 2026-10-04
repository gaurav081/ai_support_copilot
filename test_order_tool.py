from app.tools.orders import get_order_status


result = get_order_status("ORD1001")

print("\nOrder information:")
print(result)