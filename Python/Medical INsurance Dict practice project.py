# Add your code here
medical_costs = {}

#agrego key:value de a una
medical_costs["Marina"] = 6607.0
medical_costs["Vinay"] = 3225.0

#update method  para agregar multiples key:value 
medical_costs.update({"Connie": 8886.0, "Isaac": 16444.0, "Valentina": 6420.0})
# print(medical_costs)

#para corregur, reescribo el valor especificando la key
medical_costs["Vinay"] = 3325.0
# print(medical_costs)


total_cost  = 0
for value in medical_costs.values():
  total_cost += value
  #puedo imprimir cada valor si quisiera, con el prin dentro del fos en este caso
  #print(value)
average_cost = total_cost /len(medical_costs)
# print(f"Average Insurance Cost: {average_cost}")


names = ["Marina", "Vinay", "Connie", "Isaac", "Valentina"]
ages = [27, 24, 43, 35, 52]
#las dos lineas de abajo hacen exactamente lo mismo que las 3 de abajo, solo que en un paso menos
#zipped_ages  = {key:value for key, value in zip(names, ages)}
#print(zipped_ages)

zipped_ages  = zip(names, ages)
names_to_ages = {key:value for key, value in zipped_ages}
# print(names_to_ages)

# get para extraer el valor de mi key "Marina", y dejo el None por defecto si no existe ese valor
marina_age = names_to_ages.get("Marina", None)
# print(f"Marina's age is {marina_age}")

# re un diccnario y luego le agrego la key "Marina" con un valor igual a un nuevo dict con data medica
medical_records = {}
medical_records["Marina"] = {"Age": 27, "Sex": "Female", "BMI": 31.1, "Children": 2, "Smoker": "Non-smoker", "Insurance_cost": 6607.0}
#hago lo mismo con otros pacientes , sienod cada nombre una key
medical_records["Vinay"] = {"Age": 24, "Sex": "Male", "BMI": 26.9, "Children": 0, "Smoker": "Non-smoker", "Insurance_cost": 3225.0}
medical_records["Connie"] = {"Age": 43, "Sex": "Female", "BMI": 25.3, "Children": 3, "Smoker": "Non-smoker", "Insurance_cost": 8886.0}
medical_records["Isaac"] = {"Age": 35, "Sex": "Male", "BMI": 20.6, "Children": 4, "Smoker": "Smoker", "Insurance_cost": 16444.0}
medical_records["Valentina"] = {"Age": 52, "Sex": "Female", "BMI": 18.7, "Children": 1, "Smoker": "Non-smoker", "Insurance_cost": 6420.0}
# print(medical_records)

# print(f"Connie's insurance cost is {medical_records["Connie"]["Insurance_cost""]} dollars.")
# La frase de arriba tiene un problema de sintaxis porque las comillas dobles dentro de la f-string entran en conflicto con las comillas dobles que delimitan la expresión. Para que funcione correctamente, necesitas usar comillas simples para las claves dentro del diccionario, así:
# print(f"Connie's insurance cost is {medical_records['Connie']['Insurance_cost']} dollars.")


# metodo .pop para borrar una key especifica, en este caso la key "Vinay"
medical_records.pop("Vinay")


for name, record in medical_records.items():
    print(f"{name} is a {record['Age']} year old {record['Sex']} {record['Smoker']} with a BMI of {record['BMI']} and insurance cost of {record['Insurance_cost']}")