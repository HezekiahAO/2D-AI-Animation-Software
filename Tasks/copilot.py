def get_scores():
    students = (
        {"name": "Alice", "scores": [70, 80, 90]},
        {"name": "Bob", "scores": [60, 75, 85]},
        {"name": "David", "scores": [50, 23, 90]},
        {"name": "Hezekiah", "scores": [100, 100, 100]}
    )

    for student in students:          # Gose through the dict Alice and then Bod
        for score in student["scores"]:   # Goes through their scores

            yield student["name"], score  # Gives out both socres and name

# Calling the get_score function 
for name, score in get_scores():
    print(name, score)


# Recursive funtion to compute the average score

def get_students():
    students = (
        {"name": "Alice", "scores": [70, 80, 90]},
        {"name": "Bob", "scores": [60, 75, 85]},
        {"name": "David", "scores": [50, 23, 90]},
        {"name": "Hezekiah", "scores": [100, 100, 100]})
    
    for student in students:
            yield student # yield each full student dictionary 

def average_score(students):
    scores = students["scores"] # access the list of scores at the beginning and gets the required value
    length = len(scores) # I used this to get the length of the student scores
    total = sum(scores)  # Sums the total length of the scores
    average = total / length
    
    print(f"This is {student['name']} average score:  {average}")   # This takes the entire list of students, and pick out each student one by one and getting their average

for student in get_students():   
    average_score(student)    


import time  # Optional, for adding delays between retries

# Retry decorator
def retry_decorator(retries=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < retries - 1:
                        time.sleep(delay)  # Optional delay between retries
            raise Exception(f"Function {func.__name__} failed after {retries} retries.")
        return wrapper
    return decorator

# Example function to demonstrate the retry decorator
@retry_decorator(retries=3, delay=2)
def example_function():
    print("Trying to execute function...")
    raise ValueError("Simulated error")  # Simulate an exception

# Call the decorated function
try:
    example_function()
except Exception as e:
    print(e)