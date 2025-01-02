# names of hurricanes
names = [
    "Cuba I",
    "San Felipe II Okeechobee",
    "Bahamas",
    "Cuba II",
    "CubaBrownsville",
    "Tampico",
    "Labor Day",
    "New England",
    "Carol",
    "Janet",
    "Carla",
    "Hattie",
    "Beulah",
    "Camille",
    "Edith",
    "Anita",
    "David",
    "Allen",
    "Gilbert",
    "Hugo",
    "Andrew",
    "Mitch",
    "Isabel",
    "Ivan",
    "Emily",
    "Katrina",
    "Rita",
    "Wilma",
    "Dean",
    "Felix",
    "Matthew",
    "Irma",
    "Maria",
    "Michael",
]

# months of hurricanes
months = [
    "October",
    "September",
    "September",
    "November",
    "August",
    "September",
    "September",
    "September",
    "September",
    "September",
    "September",
    "October",
    "September",
    "August",
    "September",
    "September",
    "August",
    "August",
    "September",
    "September",
    "August",
    "October",
    "September",
    "September",
    "July",
    "August",
    "September",
    "October",
    "August",
    "September",
    "October",
    "September",
    "September",
    "October",
]

# years of hurricanes
years = [
    1924,
    1928,
    1932,
    1932,
    1933,
    1933,
    1935,
    1938,
    1953,
    1955,
    1961,
    1961,
    1967,
    1969,
    1971,
    1977,
    1979,
    1980,
    1988,
    1989,
    1992,
    1998,
    2003,
    2004,
    2005,
    2005,
    2005,
    2005,
    2007,
    2007,
    2016,
    2017,
    2017,
    2018,
]

# maximum sustained winds (mph) of hurricanes
max_sustained_winds = [
    165,
    160,
    160,
    175,
    160,
    160,
    185,
    160,
    160,
    175,
    175,
    160,
    160,
    175,
    160,
    175,
    175,
    190,
    185,
    160,
    175,
    180,
    165,
    165,
    160,
    175,
    180,
    185,
    175,
    175,
    165,
    180,
    175,
    160,
]

# areas affected by each hurricane
areas_affected = [
    ["Central America", "Mexico", "Cuba", "Florida", "The Bahamas"],
    ["Lesser Antilles", "The Bahamas", "United States East Coast", "Atlantic Canada"],
    ["The Bahamas", "Northeastern United States"],
    ["Lesser Antilles", "Jamaica", "Cayman Islands", "Cuba", "The Bahamas", "Bermuda"],
    ["The Bahamas", "Cuba", "Florida", "Texas", "Tamaulipas"],
    ["Jamaica", "Yucatn Peninsula"],
    ["The Bahamas", "Florida", "Georgia", "The Carolinas", "Virginia"],
    ["Southeastern United States", "Northeastern United States", "Southwestern Quebec"],
    ["Bermuda", "New England", "Atlantic Canada"],
    ["Lesser Antilles", "Central America"],
    ["Texas", "Louisiana", "Midwestern United States"],
    ["Central America"],
    ["The Caribbean", "Mexico", "Texas"],
    ["Cuba", "United States Gulf Coast"],
    ["The Caribbean", "Central America", "Mexico", "United States Gulf Coast"],
    ["Mexico"],
    ["The Caribbean", "United States East coast"],
    ["The Caribbean", "Yucatn Peninsula", "Mexico", "South Texas"],
    ["Jamaica", "Venezuela", "Central America", "Hispaniola", "Mexico"],
    ["The Caribbean", "United States East Coast"],
    ["The Bahamas", "Florida", "United States Gulf Coast"],
    ["Central America", "Yucatn Peninsula", "South Florida"],
    ["Greater Antilles", "Bahamas", "Eastern United States", "Ontario"],
    ["The Caribbean", "Venezuela", "United States Gulf Coast"],
    ["Windward Islands", "Jamaica", "Mexico", "Texas"],
    ["Bahamas", "United States Gulf Coast"],
    ["Cuba", "United States Gulf Coast"],
    ["Greater Antilles", "Central America", "Florida"],
    ["The Caribbean", "Central America"],
    ["Nicaragua", "Honduras"],
    [
        "Antilles",
        "Venezuela",
        "Colombia",
        "United States East Coast",
        "Atlantic Canada",
    ],
    [
        "Cape Verde",
        "The Caribbean",
        "British Virgin Islands",
        "U.S. Virgin Islands",
        "Cuba",
        "Florida",
    ],
    [
        "Lesser Antilles",
        "Virgin Islands",
        "Puerto Rico",
        "Dominican Republic",
        "Turks and Caicos Islands",
    ],
    ["Central America", "United States Gulf Coast (especially Florida Panhandle)"],
]

# damages (USD($)) of hurricanes
damages = [
    "Damages not recorded",
    "100M",
    "Damages not recorded",
    "40M",
    "27.9M",
    "5M",
    "Damages not recorded",
    "306M",
    "2M",
    "65.8M",
    "326M",
    "60.3M",
    "208M",
    "1.42B",
    "25.4M",
    "Damages not recorded",
    "1.54B",
    "1.24B",
    "7.1B",
    "10B",
    "26.5B",
    "6.2B",
    "5.37B",
    "23.3B",
    "1.01B",
    "125B",
    "12B",
    "29.4B",
    "1.76B",
    "720M",
    "15.1B",
    "64.8B",
    "91.6B",
    "25.1B",
]

# deaths for each hurricane
deaths = [
    90,
    4000,
    16,
    3103,
    179,
    184,
    408,
    682,
    5,
    1023,
    43,
    319,
    688,
    259,
    37,
    11,
    2068,
    269,
    318,
    107,
    65,
    19325,
    51,
    124,
    17,
    1836,
    125,
    87,
    45,
    133,
    603,
    138,
    3057,
    74,
]


# 1
# Update Recorded Damages
def update_damages(damages):
    conversion = {"M": 1000000, "B": 1000000000}
    updated_damages = []

    for damage in damages:
        if damage == "Damages not recorded":
            updated_damages.append(damage)
        else:
            value = float(damage[:-1])  # Extract the numeric part
            suffix = damage[-1]  # Extract the suffix ('M' or 'B')
            updated_damages.append(value * conversion[suffix])
    return updated_damages


# test function by updating damages
damages = [
    "Damages not recorded",
    "100M",
    "Damages not recorded",
    "40M",
    "27.9M",
    "5M",
    "Damages not recorded",
    "306M",
    "2M",
    "65.8M",
    "326M",
    "60.3M",
    "208M",
    "1.42B",
    "25.4M",
    "Damages not recorded",
    "1.54B",
    "1.24B",
    "7.1B",
    "10B",
    "26.5B",
    "6.2B",
    "5.37B",
    "23.3B",
    "1.01B",
    "125B",
    "12B",
    "29.4B",
    "1.76B",
    "720M",
    "15.1B",
    "64.8B",
    "91.6B",
    "25.1B",
]
updated_damages = update_damages(damages)
print(updated_damages)


# 2
# Create a Table
def construct_hurricane_dict(
    names, months, years, max_sustained_winds, areas_affected, damages, deaths
):
    hurricanes = {}

    for i in range(len(names)):
        hurricane_info = {
            "Name": names[i],
            "Month": months[i],
            "Year": years[i],
            "Max Sustained Wind": max_sustained_winds[i],
            "Areas Affected": areas_affected[i],
            "Damage": damages[i],
            "Deaths": deaths[i],
        }
        hurricanes[names[i]] = hurricane_info

    return hurricanes


# Test the function
hurricanes = construct_hurricane_dict(
    names, months, years, max_sustained_winds, areas_affected, updated_damages, deaths
)
print(hurricanes)


# 3
# Organizing by Year
# create a new dictionary of hurricanes with year and key
def organize_by_year(hurricanes):
    hurricanes_by_year = {}

    for hurricane in hurricanes.values():
        year = hurricane["Year"]
        if year not in hurricanes_by_year:
            hurricanes_by_year[year] = []
        hurricanes_by_year[year].append(hurricane)

    return hurricanes_by_year


# Test the function
hurricanes_by_year = organize_by_year(hurricanes)
print(hurricanes_by_year)


# 4
# Counting Damaged Areas
# create dictionary of areas to store the number of hurricanes involved in
def count_affected_areas(hurricanes):
    affected_areas_count = {}

    for hurricane in hurricanes.values():
        for area in hurricane["Areas Affected"]:
            if area not in affected_areas_count:
                affected_areas_count[area] = 1
            else:
                affected_areas_count[area] += 1

    return affected_areas_count


# Test the function
affected_areas_count = count_affected_areas(hurricanes)
print(affected_areas_count)


# 5
# Calculating Maximum Hurricane Count
# find most frequently affected area and the number of hurricanes involved in
def find_most_affected_area(affected_areas_count):
    max_area = None
    max_area_count = 0

    for area, count in affected_areas_count.items():
        if count > max_area_count:
            max_area = area
            max_area_count = count

    return max_area, max_area_count


# Test the function
most_affected_area, most_affected_count = find_most_affected_area(affected_areas_count)
print(
    f"The most affected area is {most_affected_area}, hit {most_affected_count} times."
)


# 6
# Calculating the Deadliest Hurricane
# find highest mortality hurricane and the number of deaths
def find_deadliest_hurricane(hurricanes):
    max_mortality_cane = None
    max_mortality = 0

    for hurricane in hurricanes.values():
        if hurricane["Deaths"] > max_mortality:
            max_mortality_cane = hurricane["Name"]
            max_mortality = hurricane["Deaths"]

    return max_mortality_cane, max_mortality


# Test the function
deadliest_hurricane, death_count = find_deadliest_hurricane(hurricanes)
print(
    f"The deadliest hurricane is {deadliest_hurricane}, causing {death_count} deaths."
)


# 7
# Rating Hurricanes by Mortality
# categorize hurricanes in new dictionary with mortality severity as key
def rate_hurricanes_by_mortality(hurricanes):
    mortality_scale = {0: 0, 1: 100, 2: 500, 3: 1000, 4: 10000}
    hurricanes_by_mortality = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

    for hurricane in hurricanes.values():
        deaths = hurricane["Deaths"]
        for rating, upper_bound in mortality_scale.items():
            if deaths > upper_bound:
                continue
            hurricanes_by_mortality[rating].append(hurricane)
            break
        else:
            hurricanes_by_mortality[5].append(hurricane)

    return hurricanes_by_mortality


# Test the function
hurricanes_by_mortality = rate_hurricanes_by_mortality(hurricanes)
print(hurricanes_by_mortality)


# 8 Calculating Hurricane Maximum Damage
# find highest damage inducing hurricane and its total cost
def find_most_damaging_hurricane(hurricanes):
    max_damage_cane = None
    max_damage = 0

    for hurricane in hurricanes.values():
        damage = hurricane["Damage"]
        if damage != "Damages not recorded" and damage > max_damage:
            max_damage_cane = hurricane["Name"]
            max_damage = damage

    return max_damage_cane, max_damage


# Test the function
most_damaging_hurricane, damage_cost = find_most_damaging_hurricane(hurricanes)
print(
    f"The most damaging hurricane is {most_damaging_hurricane}, causing ${damage_cost} in damages."
)


# 9
# Rating Hurricanes by Damage
# categorize hurricanes in new dictionary with damage severity as key
def rate_hurricanes_by_damage(hurricanes):
    damage_scale = {0: 0, 1: 100000000, 2: 1000000000, 3: 10000000000, 4: 50000000000}
    hurricanes_by_damage = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

    for hurricane in hurricanes.values():
        damage = hurricane["Damage"]
        if damage == "Damages not recorded":
            continue
        for rating, upper_bound in damage_scale.items():
            if damage > upper_bound:
                continue
            hurricanes_by_damage[rating].append(hurricane)
            break
        else:
            hurricanes_by_damage[5].append(hurricane)

    return hurricanes_by_damage


# Test the function
hurricanes_by_damage = rate_hurricanes_by_damage(hurricanes)
print(hurricanes_by_damage)
