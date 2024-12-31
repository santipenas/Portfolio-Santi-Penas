
# as part of the Python list practice, here we have a list of medical records that contain names and insurance costs.

names = ["Mohamed", "Sara", "Xia", "Paul", "Valentina", "Jide", "Aaron", "Emily", "Nikita", "Paul"]
insurance_costs = [13262.0, 4816.0, 6839.0, 5054.0, 14724.0, 5360.0, 7640.0, 6072.0, 2750.0, 12064.0]

#append
names.append("Priscilla")
insurance_costs.append(8320.0)

#list zip method

medical_records = list(zip(insurance_costs, names))
print(medical_records)

#length
num_medical_records = len(medical_records)
print(f" There are {num_medical_records} medical records")

#Selecting List Elements via list indexes
first_medical_record = medical_records[0]
print(f"Here is the first medical record: {first_medical_record}")

#Sorting and Ordering Lists
medical_records.sort()
print(f"Here are the medical records sorted by insurance cost: {medical_records}")

#Slicing List
cheapest_three = medical_records[:3] # primeros 3 o 3 mas baratos
print(f"Here are the three cheapest insurance costs in our medical records: {cheapest_three}")

priciest_three = medical_records[-3:] # ultimos 3 o 3 mas caros
print(f"Here are the three most expensive insurance costs in our medical records: {priciest_three}")


#Counting Elements in a List
#chequea valor boleano si "Paul" se encuentra en names
occurrences_paul = "Paul" in names 
print(occurrences_paul) 

#cuenta la cantidad de veces que "Paul" se repite dentro de names
occurrences_paul_b =  names.count("Paul")
print(f"There are {occurrences_paul_b} individuals with the name Paul in our medical records.")
