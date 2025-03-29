#A simple Python program that checks whether  each number form 1 - 15 is either even or odd using a loop

for i in range(1,16):   #The last number will be 15


    if i % 2 == 0:   # divisible by 2

            print("The number is even", i)

    else:
        print("The number is Odd", i)



# A simple calculator

try:  # Basic error handling using try–except 

     a = int(input("Enter a number:  "))
     b = int(input("Enter another number:  "))   # Uses input() to get two numbers from the user and convert them to integers (or floats).

     operation = input("Enter an operation +, -, *, /:  ")   # Asking the user to choose an operation by typing one of the following symbols: +, -, *, or /.



     if operation == "+":
          print( "addition =  ",a + b)

     elif operation == "-":
          print("Subtraction =   ",a-b)

     elif operation == "*":
       print("Multiplication =  ",a*b)
     else:
          print( "Divison =   ",a/b)                      # Using an if–elif–else block to perform the corresponding operation.

except ValueError:
     print("Hello :(   Please Enter only Integers. Example 3, 2, 1,")
except ZeroDivisionError:
     print("Naaaa, Please dont try to divide by zero, Use a real number!!")
