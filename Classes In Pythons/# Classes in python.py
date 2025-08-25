# Classes in python
class Animal :
    pass
class Employee:          # This is a Class Variable 


    def __init__(self, first, last, pay):
        self.first = first
        self.last = last                          #s Instance Variables
        self.pay = pay

    # Instance variables are used for datas that are uniqe for each instance created   examples are the self.first variables created and so on

    def __init__(self): # Instance 
        pass
           # the ._in python makes the variable a private 
        
        # Method have () at there ends

    #  self.first = first
    #  self.last = last
    #  self.pay = pay 
    #  self.email = fist + '.' + last + '@company.com'

       #  Class Variables
       # This are variables that are shared among all instances of a class
       # 
       # 
       # Note : The mehtod  of a class variable automatically takes in the instance 
       #  
       #  
        # Class Variable should be the same for class.
        
        # Class variables are unique for each instance.


Employee.number_of_emp = 2 # From the youtube Vid i was watching  if you examine the code quite well, you will see that Employee is the Class Variable like class Employee:
print(Employee.number_of_emp)

# Now, ANswer the Question, when is the use of Instance Variable necessary or the use of class variable necessary? ANd what are the difference?


# Class Methods, Regular Methods and Instance Methods
# Regular Methods automatically takes the instance as the first argument.
# A way to change a regualr method to a class method is by adding a decorator in the top.......  So basically, the decorator alters the functionality of the method such that we recieve our class as the first method.
# eg 
# @classmethod
# def set_raise_amt(cls, amount) the cls is the class name, we didnt use class as he name cos 1 we've used it before and 2 it is a keyword in python so that will raise an issue. Anmunt is the argument.
# so arguments ae the values you pass into a function when you call it eg

#name = input("Enter your name  ")
#age = input ("What is your age  ")



#def gestures(name, age):

    
 #   name = input("Enter your name  ")
 #   age = input ("What is your age  ")    # Why doesnt this work?

 #   print(f'Hi {name} so you are {age}')
  #  gestures(f"Hi {name} your age is stored as {age}")

# This is an example showing an Arugment age and name.


#@classmethod 
#def set_raise_amt(cls, amount):
#    cls.raise_amt = amount

# Employee.set-set_raise_amt(2)
# seting the class method to 2%

# class metods can be used as alternative constructors. 

# there is a way too such as using the split method Corey Schafer takled about this.

                                     # Static Method
# Unlike regular method that automatically passes instances as the first argument such as self in the example above, and class methods that automatically passes instances as the first argument such as cls in the example above, 
# StTIC METHOD  do not automatically pass anything as there instance.
# A giveaway is that What determines if Something is a static method is if the instance is not access any where within the function. eg

import datetime

@staticmethod
def is_workday(day):
    if day.weekday() == 5 or day.weekday() == 6 :
        return False
    else:
        return True



#  Inheritance 

# You can inherit from a class by Just creating a new class and then passing the Parent class and the instance for the new class.

# The steps/chain inheritance operates is called the method resolutional order the process of going from child class to the parent class when looking for a result/attribute

class Employee:
    
    raise_ant = 1.02

    def __init__(self):
        pass

class Singner(Employee):
    pass
print(help(Singner))

employees = 'employees'
class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):  # The self in the method of this class is a reference to the instance of the class,  those first man, last name, pay are the instance of the class
                                                           # You use self to access attributes and methods of the object from within the class
        super().__init__(first, last, pay)  # Super() tells pythin to go to the parent class (Employee)
                                            # __init__() calls the employee constructor with the need values.  The __init__ is called a constructor.  a speccial method in python classes

        if employees is None:
            self.employees = []
        else:
            self.employees = employees 

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)  # This function adds employe to the list.

    def remove_emp(self, emp):
        if emp not in self.employees:
            self.employees.remove(emp)  # This function removes employe from the list.


    def print_emp(self):
        for emp in self.employees:
            print('-------->', emp.fullname())

man = Manager('David', 'man', 'emm', 9000)
                                    # The error takes 1 positional argument but 2 were given means when we defined the function, it was only one argument (Piece of data given to a function so it can fo its job)
                                    # when we were defining the function, we only provide 1 data for it to work on (Argument) but when we called it, we where calling 2 datas (Arguments). 
print(man.raise_ant)
        # The use of is sub class

class Dev():
    pass
 # dog = Dog()  Create a new instance(Instance Variable) Dog cos it has () at the end. Usually, it ould just be a vairable dog = Dog   what is d.bark () called?
 
 