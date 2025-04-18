print("Please Before you enter your Password, Ensure to include a symbol, a digit and at least an Upper Case. Thank you")

password = input("Enter your Password:  ")
    # print(type(x))
    # print(len(x))

import string   # This is what allowes me to test for symbols in this code 

special_symbol = string.punctuation   

def password_checker(password):

    s1 = any(char.isupper() for char in password)
    s2 = any(char.isdigit() for char in password)
    s3 = any(char in special_symbol for char in password) # s1, s2, s3 stands for strength 1,2,3 respectivly. 





    strength = sum(s1,s2,s3)
    
    if strength >= 3 and len(password) >=8:
        print("Password Strength is Strong   ")

    elif strength == 2 and len(password) >=8:
      print("Password has medium Strength   ")
    
    else:
        print("Your Password is Weak   ")    #This aspect of code is specifically testing the strength of the password

    
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
        
