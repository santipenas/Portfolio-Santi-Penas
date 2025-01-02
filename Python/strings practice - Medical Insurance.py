
#defino un string con datos de pacientes, separados por coma y punto y coma, con un # que separa el costo de la consulta
medical_data = \
"""Marina Allison   ,27   ,   31.1 , 
#7010.0   ;Markus Valdez   ,   30, 
22.4,   #4050.0 ;Connie Ballard ,43 
,   25.3 , #12060.0 ;Darnell Weber   
,   35   , 20.6   , #7500.0;
Sylvie Charles   ,22, 22.1 
,#3022.0   ;   Vinay Padilla,24,   
26.9 ,#4620.0 ;Meredith Santiago, 51   , 
29.3 ,#16330.0;   Andre Mccarty, 
19,22.7 , #2900.0 ; 
Lorena Hodson ,65, 33.1 , #19370.0; 
Isaac Vu ,34, 24.8,   #7045.0"""

# Add your code here
# print(medical_data)

#replace() para reemplazar 
updated_medical_data = medical_data.replace("#", "$")
# print(updated_medical_data)

#ver al cantidad de registros dentro demi string con for
num_records = 0
for i in updated_medical_data:
  if i == "$":
    num_records += 1
# print(f"There are {num_records} medical records in the data.")

# split(";") will create a separate item in the list each time ";" occurs in the string
medical_data_split = updated_medical_data.split(";")
# print(medical_data_split)

#defino una lista vacia, qu luego llenaré con for y .append
medical_records = []
for record in medical_data_split:
  medical_records.append(record.split(","))
# print(medical_records)

medical_records_clean = []
# outside loop that goes through each record in medical_records
for record in medical_records:
  # empty list that will store each cleaned record
  record_clean = []
  # nested loop to go through each item in each medical record
  for item in record:
    # cleaning the whitespace for each record using item.strip()
    record_clean.append(item.strip())
  medical_records_clean.append(record_clean)
#print final, casi siempre va fuera del bucle for
# print(medical_records_clean) 

# ya tengo toda la data limpia, puedo por eejmplo imprimir los nombres de los 10 induviduso dentro de mis registros, ya que el nombre corresponde al index[o] dentro de medical_records_clean y puedo acceder a este con el for siguiente:
for record in medical_records_clean:
   print(record[0].upper())

names = []
ages = []
bmis = []
insurance_costs = []

for record in medical_records_clean:
  names.append(record[0])
  ages.append(record[1])
  bmis.append(record[2])
  insurance_costs.append(record[3])
  
print(f"Names: {names}")
print(f"Ages: {ages}")
print(f"BMI: {bmis}")
print(f"Insurance Costs: {insurance_costs}")


total_bmi = 0
for bmi in bmis:
  total_bmi += float(bmi)
  average_bmi = total_bmi / len(bmis)
print(f"Average BMI: {average_bmi}")


