names = ["Judith", "Abel", "Tyson", "Martha", "Beverley", "David", "Anabel"]
estimated_insurance_costs = [1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0]
actual_insurance_costs = [1100.0, 2200.0, 3300.0, 4400.0, 5500.0, 6600.0, 7700.0]

# we have  we can iterate through the list of names and estimated insurance costs to calculate the average insurance cost in our dataset. We can also compare each actual insurance cost to the estimated insurance cost to determine how far off the estimate was from the actual cost.

total_cost = 0

# iterate through actual_insurance_costs and add each insurance cost to the variable
# total_cost.
for item in actual_insurance_costs:
    total_cost += item
    average_cost = total_cost / len(actual_insurance_costs)
# print(average_cost)
print(f"Average Insurance Cost: {average_cost} dollars.")


# range in loops
for i in range(len(names)):
    name = names[i]
    insurance_cost = actual_insurance_costs[i]
    print(f"The insurance cost for {name} is {insurance_cost} dollars.")

    # conditional inside loops
    if insurance_cost > average_cost:
        print(f"The insurance cost for {name} is above average.")
    elif insurance_cost < average_cost:
        print(f"The insurance cost for {name} is below average.")
    else:
        print(f"The insurance cost for {name} is equal to average.")

# list coprehension
updated_estimated_costs = [
    estimated_cost * 11 / 10 for estimated_cost in estimated_insurance_costs
]
print(updated_estimated_costs)
