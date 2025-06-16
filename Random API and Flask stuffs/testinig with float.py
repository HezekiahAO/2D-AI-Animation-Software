x = float(input("Enter a value:   "))
y = float(input("Enter a value:   "))

try: 
    operations = input("Enter an Operation  ")
    if operations == "Addition":    # You have defined it already with = now, make it equals to with ==
            print("Answer is ",x+y)
    else:
         print("I will do subtraction which is ", x-y)        
except ValueError:
    print("I am sorry, i cant do that")