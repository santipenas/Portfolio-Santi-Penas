
#lets practice creating a class and methods to estimate the insurance cost of a patient and formulating a patient profile with methods to update the patient's age and number of children.

class Patient:
    # Constructor method
    def __init__(self, name, age, sex, bmi, num_of_children, smoker):
        self.name = name
        self.age = age
        self.sex = sex
        self.bmi = bmi
        self.num_of_children = num_of_children
        self.smoker = smoker

    # Method to estimate insurance cost
    def estimated_insurance_cost(self):
        estimated_cost = (250 * self.age - 128 * self.sex + 370 * self.bmi + 425 * self.num_of_children + 24000 * self.smoker - 12500)
        print(f"{self.name}'s estimated insurance cost is {estimated_cost} dollars.")

    # Method to update the patient's age
    def update_age(self, new_age):
        self.age = new_age
        print(f"{self.name} is now {self.age} years old.")

    # Method to update the number of children
    def update_num_children(self, new_num_children):
        self.num_of_children = new_num_children
        print(f"{self.name} has {self.num_of_children} children.")
    
    def patient_profile(self):
      # we initialize an empty dictionary
        patient_information = {}
      # we set name as a key tied with the name value
        patient_information["Name"] = self.name
        patient_information["Age"] = self.age
        patient_information["Sex"] = self.sex
        patient_information["BMI"] = self.bmi
        patient_information["Number of Children"] = self.num_of_children
        patient_information["Smoker"] = self.smoker
          
        return patient_information
  
# Create an instance of the Patient class
patient1 = Patient("John Doe", 25, 1, 22.2, 0, 0)

# Call all the methods to test them and all the updated values
patient1.estimated_insurance_cost()
# Output: John Doe's estimated insurance cost is 1836.0 dollars.

patient1.update_age(26)
# Output: John Doe is now 26 years old.

# Call the insurance cost method again to see the updated result after the age was changed
patient1.estimated_insurance_cost()

patient1.update_num_children(1)
patient1.update_num_children(4)

# Call the insurance cost method again to see the updated result after the age was changed
patient1.estimated_insurance_cost()

# call the patient_profile() method and print it, because the method itself don not print the result by itself in the return
print(patient1.patient_profile())