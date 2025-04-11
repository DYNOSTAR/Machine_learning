import collections
from datetime import datetime

sales_data = []
def main():
    while True:
        # Input customer details and product info
        customer_name = input("Enter customer name (or type 'exit' to finish): ")
        if customer_name.lower() == 'exit':
            break

        customer_id = input("Enter customer ID: ")
        product_name = input("Enter product name: ")
        sale_date = input("Enter sale date (YYYY-MM-DD): ")
# Store sales data
sales_data.append({
    'customer_name': customer_name,
    'customer_id': customer_id,
    'product_name': product_name,
    'sale_date': sale_date
    })

# Calculate total sales per product
product_sales = collections.defaultdict(int)
daily_sales = collections.defaultdict(int)

for sale in sales_data:
    product_sales[sale['product_name']] += 1  # Count sales
    daily_sales[sale['sale_date']] += 1  # Count daily sales
# Display total sales per product
print("\nTotal sales per product:")
for product, count in product_sales.items():
    print(f"{product}: {count}")
# Determine the top-selling item
top_selling_product = max(product_sales, key=product_sales.get)
print(f"\nTop selling item: {top_selling_product} with {product_sales[top_selling_product]} sales")
# Display daily sales trends
print("\nDaily sales trends:")
for date, count in daily_sales.items():
    print(f"{date}: {count} sales")


if __name__ == '__main__':
    main()