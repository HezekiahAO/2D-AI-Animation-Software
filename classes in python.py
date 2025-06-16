#Classes in python: More like a blueprint for creating objects.
# Classes encapsulate data for the object and methods to manipulate that data.
#They allow that blue print to be used to create multiple objects with similar properties and behaviors.
# An instance includes Dog = goat(). Here, Dog is a variable referring to an instance of goat.
# The class is the blueprint, and the instance is the actual object created from that blueprint.
# The class defines the properties and behaviors, while the instance holds the specific data for that object.
# The class is the blueprint, and the instance is the actual object created from that blueprint.
# The class defines the properties and behaviors, while the instance holds the specific data for that object.
# and instance variable contians the data that is unique for each object.
# it has the benefit of code reusability, as the same class can be used to create multiple objects with similar properties and behaviors. YOU DOT HAVE TO REWRITE THE CODE FOR EACH OBJECT.
# A FUNTION ASSOCIATED WITH A CLASS IS CALLED A METHOD.
# A CLASS CAN HAVE MULTIPLE METHODS, AND EACH METHOD CAN HAVE ITS OWN PARAMETERS AND RETURN VALUES.
# A CLASS CAN ALSO HAVE CLASS VARIABLES, WHICH ARE SHARED AMONG ALL INSTANCES OF THE CLASS.
# CLASS VARIABLES ARE DEFINED OUTSIDE OF ANY METHOD AND ARE ACCESSIBLE TO ALL INSTANCES OF THE CLASS.
# A CLASS CAN ALSO HAVE INSTANCE VARIABLES, WHICH ARE UNIQUE TO EACH INSTANCE OF THE CLASS.
# Here is an example

class Places:
    pass   
class Places:
    def __aninstance__(self):
        self.name= "is an instance variable while specifying what this particular value represents"  " Like what a normal variable does but this on is for a class (label)"
        self.school = "Another One"
        self.location = input(str('Enter Your Location make i coe find you'))

    def fullname(self):  #Passed the same instance here self
        return("Hezekaih".format(self))