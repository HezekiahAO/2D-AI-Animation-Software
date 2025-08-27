# Create a list of dictionaries to store the report data    

student = [
    {"name": "Alice", "age": 20, "grade": 'A' "score": {[90, 99, 87]} },   # name is writen like this because it indicate it's a string literal:::: name  is often used as a key that maps to some value
    {"name": "David", "age": 22, "grade": 'B'  'score': [85, 88, 90]},
    {"name": "Charlie", "age": 21, "grade": 'C'},            # Created a dictionary with keys and values to store student data
]



def fetch():
    for items in student:
         yield items # Using yield to create a generator that yields each item in the student list


# Recursion in Python is a programming technique where a function calls itself during its execution to solve a problem
def get_score(name, score):
    for i in student:
        print(f"Name: {i['name']}, Age: {i['age']}, Grade: {i['grade']}")
