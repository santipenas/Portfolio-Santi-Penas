
#lest practice functions with a medical insurance cost calculator



# Create calculate_insurance_cost() function below: 
def calculate_insurance_cost(name, age, sex, bmi, num_of_children, smoker):
  estimated_cost = 250*age - 128*sex + 370*bmi + 425*num_of_children + 24000*smoker - 12500
  print(f"The estimated insurance cost for {name} is {estimated_cost}  dollars.")
  return estimated_cost
  

# Estimate Maria's insurance cost
maria_insurance_cost = calculate_insurance_cost("Maria", 28, 0, 26.2, 3, 0)
#Salida: The estimated insurance cost for Maria is 5469.0  dollars.


# Estimate Omar's insurance cost 
omar_insurance_cost = calculate_insurance_cost("Omar", 35, 1, 22.2, 0, 1)
#Salida: The estimated insurance cost for Omar is 28336.0  dollars.


# my personal insurance cost
my_insurance_cost = calculate_insurance_cost("Santiago", 22, 1, 19.2, 0, 1)
#Salida: The estimated insurance cost for Santiago is 23976.0  dollars.