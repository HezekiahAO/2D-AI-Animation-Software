def get_score():
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
for name, score in get_score():
    print(name, score)


# Recursive funtion to compute the average score
def average_score(students):
    length = len(students)
    sum = sum(students)

    x = sum("scores")/length("score")
    print("The Average score of the students is " ,x)