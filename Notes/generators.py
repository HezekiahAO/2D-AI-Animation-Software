# recursions in python
# This is more like you are calling a function form it self like a mistake i did by calling a fuction from itself eg

#def say():
# print("Hello")
#   say()

#This is a recursive function

import sys
sys.setrecursionlimit(2000)

# I can adjust the recusion limit by say sys.setrecusionlimit(then put in the number you want)

i = 0
def greet():
    global i
    print("Hello", i)
    i += 1
    greet()   # This is the part where i cal the fuction inside the function
greet()


#The error local variable 'i' referenced before assignment  can be fixd with calling i a global value as used in the example


# Decorators in python
#  Decorators in Python are a powerful feature that let you modify or extend the behavior of functions or classes without changing their actual code. 
# They’re often used for logging, access control, memoization, and more.
# The decorator wraps your function with extra behavior.

print(5)

def value_1():
    yield 9


gen = value_1()
print(next(gen))


# Yes! In Python, generators are a type of iterable that allow you to iterate over a sequence of values lazily. This means they generate values one at a time as needed, rather than storing the entire sequence in memory at once. This can be very useful when working with large data sets)

print(5)

def value():
    yield 9

for v in value():
    print(v)
