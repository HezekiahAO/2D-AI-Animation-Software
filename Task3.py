#A simple Python program that checks whether  each number form 1 - 15 is either even or odd

for i in range(1,16):


    if i % 2 == 0:

            print("The number is even", i)

    else:
        print("The number is Odd", i)



# A simple calculator

a = input(int("Enter a number"))
b = input(int("Enter another number"))

operation = input("Enter an operation +, -, *, /")
if operation == "+":
   print(a + b)

elif operation == "-":
     print(a-b)

elif operation == "*":
    print(a*b)
else:
     print(a/b)