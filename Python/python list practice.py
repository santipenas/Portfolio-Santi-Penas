inventory = ["twin bed", "twin bed", "headboard", "queen bed", "king bed", "dresser", 
"dresser", "table", "table", "nightstand", "nightstand", "king bed", "king bed", 
"twin bed", "twin bed", "sheets", "sheets", "pillow", "pillow"]

# Checkpoint 1
inventory_len = len(inventory)

# Checkpoint 2
first = inventory[0]

# Checkpoint 3
last = inventory[-1]

# Checkpoint 4
inventory_2_6 = inventory[2:6]

# Checkpoint 5
first_3 = inventory[:3]

# Checkpoint 6
twin_beds = inventory.count("twin bed")

# Checkpoint 7
removed_item = inventory.pop(4)

# Checkpoint 8
inventory.insert(10, "19th Century Bed Frame")

#Checkpoint 9
inventory.sort()
print(inventory)