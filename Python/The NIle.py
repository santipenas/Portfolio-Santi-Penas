

# The NIle.py para practicar funciones

import math

# Constantes simuladas
SHIPPING_PRICES = {
    "standard": 1.0,
    "express": 1.5,
    "overnight": 2.0
}

# Función para calcular distancia entre dos puntos
def get_distance(from_lat, from_long, to_lat, to_long):
    return math.sqrt((to_lat - from_lat)**2 + (to_long - from_long)**2)

# Función para formatear el precio
def format_price(price):
    return f"${price:.2f}"

# Simulación del módulo test
def test_function(func):
    print(f"Testing {func.__name__}...")
    print("Test passed!\n")

# Define calculate_shipping_cost() aquí:
def calculate_shipping_cost(from_coords, to_coords, shipping_type):
    from_lat, from_long = from_coords
    to_lat, to_long = to_coords
    distance = get_distance(from_lat, from_long, to_lat, to_long)
    shipping_rate = SHIPPING_PRICES[shipping_type]
    price = distance * shipping_rate
    return format_price(price)

# Test the function llamándola
test_function(calculate_shipping_cost)

# Define calculate_driver_cost() aquí:
def calculate_driver_cost(distance, *drivers):
    cheapest_driver = None
    cheapest_driver_price = None
    for driver in drivers:
        driver_time = distance / driver["speed"]
        price_for_driver = driver["salary"] * driver_time
        if cheapest_driver is None:
            cheapest_driver = driver
            cheapest_driver_price = price_for_driver
        elif price_for_driver < cheapest_driver_price:
            cheapest_driver = driver
            cheapest_driver_price = price_for_driver
    return cheapest_driver_price, cheapest_driver

# Test the function llamándola
test_function(calculate_driver_cost)

# Define calculate_money_made() aquí:
def calculate_money_made(**trips):
    total_money_made = 0
    for trip_id, trip in trips.items():
        trip_revenue = trip["cost"] - trip["driver"]["cost"]
        total_money_made += trip_revenue
    return total_money_made

# Test the function llamándola
test_function(calculate_money_made)
