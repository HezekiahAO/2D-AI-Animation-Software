print("Please Before you enter your Password, Ensure to include a symbol, a digit and at least an Upper Case. Thank you")

password = input("Enter your Password:  ")
    # print(type(x))
    # print(len(x))

import string

special_symbol = string.punctuation


if len(password) < 8:
    print("Please enter an 8 digit passeword or more:    ")

elif any(char.isupper() for char in password) == False :
    print("Please include at least an upper Case in your password  ")


elif any(char.isdigit() for char in password) == False :
    print("Please include at least a digit in your password  ")


elif any(char in special_symbol for char in password) == False :
    print("Please include a Special Character in your password.   Na for security :) ")

else:
    print("Your Password has been Created!  ")