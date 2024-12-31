# Checkpoint 1b
import itertools


max_money = 15
options = []

# Checkpoint 1
cat_toys = [("laser", 1.99), ("scratcher", 10.99), ("fountain", 5.99), ("catnip", 15.99)]

# Checkpoint 2
cat_toy_iterator = iter(cat_toys)


# Checkpoint 3
print(next(cat_toy_iterator))
print(next(cat_toy_iterator))
print(next(cat_toy_iterator))
print(next(cat_toy_iterator))

# Checkpoint 5
toy_combos = itertools.combinations(cat_toys, 2)

# Checkpoint 6
for combo in toy_combos:
    toy1 = combo[0]
    cost_of_toy1 = toy1[1]
    toy2 = combo[1]
    cost_of_toy2 = toy2[1]
    if cost_of_toy1 + cost_of_toy2 <= max_money:
      options.append(combo)
      
# Checkpoint 7
print(options)