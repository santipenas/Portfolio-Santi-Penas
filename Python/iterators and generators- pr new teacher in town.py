# practicamos iterators y generators

import itertools

# Define the ClassroomOrganizer class
class ClassroomOrganizer:
    def __init__(self, students):
        # Store students and sort them alphabetically by the "name" key
        self.students = sorted(students, key=lambda x: x["name"])
    
    def __iter__(self):
        # Initialize the iterator and return self
        self.index = 0
        return self
    
    def __next__(self):
        # Raise StopIteration when the iteration is complete
        if self.index >= len(self.students):
            raise StopIteration
        # Return the current student and increment the index
        current_student = self.students[self.index]
        self.index += 1
        return current_student 
    
    def seat_combinations(self):
        # Get all possible combinations of 2 students per table
        return list(itertools.combinations(self.students, 2))

# Student roster
student_roster = [
    {"name": "Karina M", "age": 8, "height": 48, "favorite_subject": "Math", "favorite_animal": "Dog"},
    {"name": "Yori K", "age": 7, "height": 50, "favorite_subject": "Art", "favorite_animal": "Cat"},
    {"name": "Alex C", "age": 7, "height": 47, "favorite_subject": "Science", "favorite_animal": "Cow"},
    {"name": "Esmeralda R", "age": 8, "height": 52, "favorite_subject": "History", "favorite_animal": "Rabbit"},
    {"name": "Sandy P", "age": 7, "height": 49, "favorite_subject": "Recess", "favorite_animal": "Guinea Pig"},
    {"name": "Matthew Q", "age": 7, "height": 46, "favorite_subject": "Music", "favorite_animal": "Walrus"},
    {"name": "Trudy B", "age": 8, "height": 45, "favorite_subject": "Science", "favorite_animal": "Ladybug"},
    {"name": "Benny D", "age": 7, "height": 51, "favorite_subject": "Math", "favorite_animal": "Ant"},
    {"name": "Helena L", "age": 7, "height": 53, "favorite_subject": "Art", "favorite_animal": "Butterfly"},
    {"name": "Marisol R", "age": 8, "height": 50, "favorite_subject": "Math", "favorite_animal": "Lion"}
]

# Create an instance of ClassroomOrganizer
organizer = ClassroomOrganizer(student_roster)

# Print all students using the iterator
print("Student Roster:")
for student in organizer:
    print(student)

# Get and print the combinations of seating arrangements
print("\nSeating Combinations:")
seating_combinations = organizer.seat_combinations()
for combo in seating_combinations:
    print(combo)
