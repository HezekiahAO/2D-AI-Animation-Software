#A simple Python program that checks whether  each number form 1 - 15 is either even or odd

for i in range(1,16):


    if i % 2 == 0:

            print("The number is even", i)

    else:
        print("The number is Odd", i)



# A simple calculator

a = int(input("Enter a number:  "))
b = int(input("Enter another number:  "))

operation = input("Enter an operation +, -, *, /:  ")

if operation == "+":
   print( "addition =  ",a + b)

elif operation == "-":
     print("Subtraction =   ",a-b)

elif operation == "*":
    print("Multiplication =  ",a*b)
else:
     print( "Divison =   ",a/b)

try:
     a = int(input("Enter a number:\n"))
except ValueError:
     print("Wrong parameter to enter")
a = 0
print("The value of a is:  ", a)