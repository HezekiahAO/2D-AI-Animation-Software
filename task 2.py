x = "Send me money"

y = 21

List = ["I'm", "Hezekiah", "Ajayi-Omoleye"]


dict = {"Key" : "Value", "Per" : "Data Type", "Numbers" : 221}

set = {"Opay","Value", "Per", "Data Type"}

Money = True

cash = False

Turples_scoops = (0,9,0,6,5,2,7,1,3,4,6)

floats = 1213.4532


print(type(x))
print(type(y))
print(type(List))
print(type(dict))
print(type(set))
print(type(Money))
print(type(cash))
print(type(Turples_scoops))
print(type(floats))


# Question 2 
#Addition
a = 2
b = 3
c = a + b
print(c)

d = 11.5
e = 11.5
f = d + e
print(f)

# Subtraction

g = a - b
h = d - e
print(g)
print(h)

# Multiplcation

i = a * b
print(i)
j = d * e
print(j)

# Division

k = a // b
print(k)
m = a / b
print(m)
l = d // e
print(l)


# Question 3 Convert between different numeric types using int() and float

Number = int(29479.8883405783)
print(Number)
Number_1 = float(198)
print(Number_1)

# Question 4 Use string methods to manipulate text

greetings = str("Hi, HOW are you doing ?")
print(greetings)
print(greetings.upper())
print(greetings.lower())

# Question 5 Format strings in different ways. using f-string
x = 10
y = 20
print(f"The sum of {x} and {y} is {x + y}.")


# Quuestion 6 Create a list, access elements using indexing and slicing, and perform list operations (append, remove, pop, sort, reverse)

List_example = ["Hannah", "Daivd", "Key",["Lagos", "Abuja", "Ife",["Osun"]]]
# to confirm if its a list
print(type(List_example))

    #Indexing
List_example[2] = "Job"
    #Slicing
List_example[:5]

print(List_example)
print(List_example[3][3][0])  # Prints "Osun"

#  operations (append, remove, pop, sort, reverse) in the list
#append

List_example.append("Moses")
print(List_example)

# remove

List_example.remove("Hannah") #Removes Hannah from the List
print(List_example)

name_pop = List_example.pop()

# Sort 

numbers = [4, 1, 8, 3, 9]
numbers.sort()
print(numbers)  # [1, 3, 4, 8, 9]

numbers.reverse()

print(numbers)  # [9, 8, 4, 3, 1] -> becomes [1, 3, 4, 8, 9]



# Create a tuple, access elements, and demonstrate tuple immutability.

turple_example = (1,23,4,2,5,3,6)
turple_example.append (432)
turple_example.update (89)

# this shows the immutablity of a turple as it will print: tuple' object has no attribute 'append' and 'tuple' object has no attribute 'update'

print(type(turple_example))