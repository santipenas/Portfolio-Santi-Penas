



# Define daily_sales (datos ficticios para que el código funcione)
daily_sales = """John Doe ;,; $20.15 ;,; red ;,; 
Jane Smith ;,; $13.45 ;,; green&yellow ;,; 
Emily Johnson ;,; $15.50 ;,; blue&white ;,; 
Michael Brown ;,; $18.25 ;,; black ;,; 
Sarah Davis ;,; $22.00 ;,; red&blue ;,;"""

# Start coding below!
daily_sales_replaced = daily_sales.replace(";,;", "+")
# print(daily_sales_replaced)

daily_transactions = daily_sales_replaced.split(",")
# print(daily_transactions)

daily_transactions_split = []
for transaction in daily_transactions:
    daily_transactions_split.append(transaction.split("+"))
# print(daily_transactions_split)

transactions_clean = []
for transaction in daily_transactions_split:
    transaction_clean = []
    for data_point in transaction:
        transaction_clean.append(data_point.replace("\n", "").strip(" "))
    transactions_clean.append(transaction_clean)
# print(transactions_clean)

customers = []
sales = []
thread_sold = []

for transaction in transactions_clean:
    customers.append(transaction[0])
    sales.append(transaction[1])
    thread_sold.append(transaction[2])

# print(customers)
# print(sales)
# print(thread_sold)

total_sales = 0
for sale in sales:
    total_sales += float(sale.strip("$"))
print("Total sales:", total_sales)

# print(thread_sold)

thread_sold_split = []
for sale in thread_sold:
    for color in sale.split("&"):
        thread_sold_split.append(color)

def color_count(color):
    color_total = 0
    for thread_color in thread_sold_split:
        if color == thread_color:
            color_total += 1
    return color_total

# print(color_count('white'))

colors = ['red', 'yellow', 'green', 'white', 'black', 'blue', 'purple']

for color in colors:
    print("Thread Shed sold {0} threads of {1} thread today".format(color_count(color), color))

# print(thread_sold_split)