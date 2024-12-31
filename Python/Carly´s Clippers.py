

hairstyles = ["bouffant", "pixie", "dreadlocks", "crew", "bowl", "bob", "mohawk", "flattop"]

prices = [30, 25, 40, 20, 20, 35, 50, 35]

last_week = [2, 3, 5, 8, 4, 4, 6, 2]

# Calcula el precio total de los cortes
total_price = sum(prices)

# Calcula el precio promedio
average_price = total_price / len(prices)
print("Average Haircut Price: " + str(average_price))

# Aplica un descuento de $5 a cada precio
new_prices = [price - 5 for price in prices]
print("New Prices: " + str(new_prices))

# Calcula los ingresos totales de la semana pasada
total_revenue = sum(prices[i] * last_week[i] for i in range(len(hairstyles)))
print("Total Revenue: " + str(total_revenue))

# Calcula el ingreso diario promedio
average_daily_revenue = total_revenue / 7
print("Average Daily Revenue: " + str(average_daily_revenue))

# Encuentra los cortes que tienen un precio inferior a $30
cuts_under_30 = [hairstyles[i] for i in range(len(new_prices)) if new_prices[i] < 30]
print("Cuts Under $30: " + str(cuts_under_30))

