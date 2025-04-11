import matplotlib.pyplot as plt

def get_product_data():
    """Gets product information from the user."""
    products = []
    while True:
        product_name = input("Enter product name:")
        try:
            price = float(input(f"Enter price for {product_name}: "))
            products.append({'name': product_name, 'price': price, 'quantity_sold': 0})
        except ValueError:
            print("Invalid price. Please enter a number.")
    return products


def get_customer_data(products):
    """Gets customer purchase information from the user."""
    customers = []
    while True:
        customer_name = input("Enter customer name (or type 'done'): ")
        if customer_name.lower() == 'done':
            break
        product_choice = input("Enter product bought: ")
        try:
            quantity = int(input(f"Enter quantity of {product_choice} bought: "))
        except ValueError:
            print("Invalid quantity. Please enter a number")
            continue

        product_found = False
        for product in products:
            if product['name'].lower() == product_choice.lower():
                product['quantity_sold'] += quantity
                customers.append({'name': customer_name, 'product': product_choice, 'quantity': quantity})
                product_found = True
                break
        if not product_found:
            print(f"Product '{product_choice}' not found.")
    return customers


def calculate_daily_sales(products):
    """Calculates the total daily sales."""
    total_sales = 0
    for product in products:
        total_sales += product['price'] * product['quantity_sold']
    return total_sales


def find_most_selling_product(products):
    """Finds the product with the highest sales."""
    if not products:
        return None
    most_selling_product = max(products, key=lambda x: x['quantity_sold'])
    return most_selling_product


def plot_sales_trend(daily_sales_data):
    """Plots a line graph showing the daily sales trend."""
    days = list(range(1, len(daily_sales_data) + 1))  # Assuming sales data is collected daily
    plt.plot(days, daily_sales_data)
    plt.xlabel('Day')
    plt.ylabel('Total Sales')
    plt.title('Daily Sales Trend')
    plt.grid(True)
    plt.show()


def main():
    products = get_product_data()
    customers = get_customer_data(products)
    daily_sales = calculate_daily_sales(products)

    print("\n--- Sales Report ---")
    print(f"Total Daily Sales: ${daily_sales:.2f}")

    most_selling = find_most_selling_product(products)
    if most_selling:
        print(f"Most selling product: {most_selling['name']} ({most_selling['quantity_sold']} units)")

    # Example daily sales trend data (replace with your actual data)
    daily_sales_data = [daily_sales]  # Initialize with today's sales

    plot_sales_trend(daily_sales_data)


if __name__ == "__main__":
    main()