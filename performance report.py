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

def get_scores():
    students = (
        {"name": "Alice", "scores": [70, 80, 90]},
        {"name": "Bob", "scores": [60, 75, 85]},
        {"name": "David", "scores": [50, 23, 90]},
        {"name": "Hezekiah", "scores": [100, 100, 100]}
    )

    for student in students:
        for score in student["scores"]:
            yield score  # this is the same code form the first but i just yield scores un this to allow me to get an average


def average_score(students):

    scores = students[scores] # access the list of scores at the beginning and gets the required value

    length = len(scores) # i used this to get the length of the student scores

    total = sum(scores)  # Sums the total length of the scores

    print("Number of scores:", length)

    average = total / length
    print("The Average score of the students is " ,average)

for students in get_scores():
    average_score(students)       # This helps me loop through all the student and then compute their average score


   