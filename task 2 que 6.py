# Quuestion 6 Create a list, access elements using indexing and slicing, and perform list operations (append, remove, pop, sort, reverse)

List_example = ["Hannah", "Daivd", "Key",["Lagos", "Abuja", "Ife",["Osun"]]]
# to confirm if its a list
print(type(List_example))

    #Indexing
List_example[2] = "Job"
    #Slicing


print(List_example[:2]) #prints the first 2 elemets

print(List_example[3][3][0])  # Prints "Osun"

#  operations (append, remove, pop, sort, reverse) in the list
#append

List_example.append("Moses")
print(List_example)

# remove

List_example.remove("Hannah") #Removes Hannah from the List
print(List_example)

# pop : this removes an item of the list
remove = List_example.pop()
print(remove) #removes Moses
print(List_example)

remove_1 = List_example.pop(1)
print(remove_1) #removes Job because caounting starts from 0

print(List_example)


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