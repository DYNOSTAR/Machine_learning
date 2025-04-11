import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Connect to SQLite database (or create it)
conn = sqlite3.connect('ecommerce_sales.db')

# Create a cursor
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    product_name TEXT,
    sale_amount REAL,
    customer_details TEXT,
    sale_date TEXT
)
''')

# Function to input data
def input_sales_data():
    while True:
        product_name = input("Enter product name (or 'exit' to finish): ")
        if product_name.lower() == 'exit':
            break
        sale_amount = float(input("Enter sale amount: "))
        customer_details = input("Enter customer details: ")
        sale_date = datetime.now().strftime('%Y-%m-%d')  # Current date
        cur.execute('INSERT INTO sales (product_name, sale_amount, customer_details, sale_date) VALUES (?, ?, ?, ?)',
                    (product_name, sale_amount, customer_details, sale_date))
        conn.commit()

# Input sales data
input_sales_data()

# Query total sales per product
total_sales_query = pd.read_sql_query('SELECT product_name, SUM(sale_amount) as total_sales FROM sales GROUP BY product_name', conn)

# Display total sales per product
print("Total sales per product:")
print(total_sales_query)

# Query top selling items
top_selling_items = total_sales_query.nlargest(5, 'total_sales')
print("\nTop selling items:")
print(top_selling_items)

# Visualize sales trends
sales_data = pd.read_sql_query('SELECT sale_date, SUM(sale_amount) as total_sales FROM sales GROUP BY sale_date', conn)
sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date'])

plt.figure(figsize=(10, 5))
plt.plot(sales_data['sale_date'], sales_data['total_sales'], marker='o')
plt.title('Sales Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Close the database connection
conn.close()