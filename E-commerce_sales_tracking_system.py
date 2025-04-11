# the python script below allows an e-commerce to store and track sales transacted online
import matplotlib.pyplot as plt # matplotlib will help in generating a visualization graph of sales trend


def get_product_data(): # This function allows product data entry
    products = []
    prices = []
    num_products = int(input("Enter the number of products on sale: "))
    for i in range(num_products):
        product_name = input(f"Enter the name of product {i + 1}: ")
        price = float(input(f"Enter the price of {product_name}: "))
        products.append(product_name)
        prices.append(price)
    return products, prices


def get_customer_data(products): # This function allows customer details entry
    customer_purchases = {}
    num_customers = int(input("Enter the number of customers: "))
    for i in range(num_customers):
        customer_name = input(f"Enter name of customer {i + 1}: ")
        customer_purchases[customer_name] = []
        num_purchases = int(input(f"How many products did {customer_name} buy? "))
        for _ in range(num_purchases):
            while True:
                product_choice = input(f"Enter the product bought by {customer_name} (from {', '.join(products)}): ")
                if product_choice in products:
                    customer_purchases[customer_name].append(product_choice)
                    break
                try:
                    quantity = int(input(f"Enter quantity of {product_choice} bought in kgs: "))
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
                else:
                    print("Invalid product name. Please try again.")
    return customer_purchases


def calculate_sales(products, prices, customer_purchases): # This function allows calculation of total sales
    total_sales = 0
    product_sales = {}
    for product in products:
        product_sales[product] = 0

    for customer, purchases in customer_purchases.items():
        for product in purchases:
            total_sales += prices[products.index(product)]
            product_sales[product] += 1

    return total_sales, product_sales


def display_results(total_sales, product_sales): # Function for displaying total sales and most sold product
    print("\n--- Sales Report ---")
    print(f"Total Daily Sales: ${total_sales:.2f}")

    most_sold_product = max(product_sales, key=product_sales.get)
    print(f"Most sold product: {most_sold_product} (Quantity: {product_sales[most_sold_product]})")


def plot_sales_trend(product_sales): # Function to plot a sale trend graph
    products = list(product_sales.keys())
    sales_counts = list(product_sales.values())

    plt.figure(figsize=(10, 6))
    plt.plot(products, sales_counts, marker='o', linestyle='-')
    plt.xlabel("Products")
    plt.ylabel("Number of Sales")
    plt.title("Product Sales Trend")
    plt.grid(True)
    plt.show()


# Main execution and functions calling
products, prices = get_product_data()
customer_purchases = get_customer_data(products)
total_sales, product_sales = calculate_sales(products, prices, customer_purchases)
display_results(total_sales, product_sales)
plot_sales_trend(product_sales)