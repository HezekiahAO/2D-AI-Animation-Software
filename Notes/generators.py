print(5)

def value():
    yield 9


gen = value()
print(next(gen))


# Yes! In Python, generators are a type of iterable that allow you to iterate over a sequence of values lazily. This means they generate values one at a time as needed,
#  rather than storing the entire sequence in memory at once. This can be very useful when working with large data sets
# so you can just call a single value from the list and store it instead of calling the entire list



print(5)

def value():
    yield 9

for v in value():
    print(v)


# This is another random file



# Resurcive Funtons A recursive function in Python is a function that calls itself during its execution. 
# This allows the function to solve a problem by breaking it down into smaller, simpler subproblems.
#  A recursive function typically has two main components:
