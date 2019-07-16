#! /usr/bin/env python
import pickle

class Auto:
    def __init__(self, number_of_cylinders, color):
        self.number_of_cylinders = number_of_cylinders
        self.color = color

class Car(Auto):
    def __init__(self, color):
        Auto.__init__(self, 4, color)
Toyota_Corolla = Car("white")
print ("My Car Toyota_Corolla is {0} and has {1} cylinders".format( Toyota_Corolla.color, Toyota_Corolla.number_of_cylinders))
### Add your statements here to create a pickled object of Toyota_Corolla
car = pickle.dumps(Toyota_Corolla)
###############################################
### Add a line here to print the pickled object you just created
#print(car)
###############################################

### Add your statements here to pickle Toyota_Corolla to a .bin file
f = open("Toyota_Corolla.bin", "wb")
pickle.dump(car, f, protocol=2)
f.close()

###############################################

### Create a function that will unpickle the pickled file that is passed to it. (Same as previous but with a function)
def get_car(f):
    f.seek(0)
    pickled_car = pickle.load(f)
    car = pickle.loads(pickled_car)
    return car

f = open("Toyota_Corolla.bin", "rb")
Toyota_Corolla = get_car(f)

#print(car)
###############################################
### Use the function you wrote to unpickle the .bin file and create 2 new objects (Lexus_IS and Toyota_Camry) without changing any attributes

Lexus_IS = get_car(f)
Toyota_Camry = get_car(f)

###############################################
### Print the attributes of Lexus_IS and Toyota_Camry
#print(vars(Lexus_IS))
#print(vars(Toyota_Camry))

###############################################
### Change the color attribute of Lexus_IS to red 
### Change the color attribute of Toyota_Camry to blue and red
### Change the number of cylinders attribute of Toyota_Camry to 6
### The print the attributes of Toyota_Corolla, Toyota_Camry and Lexus_IS 

Lexus_IS.color = 'red'
Toyota_Camry.color = 'blue and red'
Toyota_Camry.number_of_cylinders = 6

###############################################
print("Lexus_IS is now {0} and still has {1} cylinders".format(Lexus_IS.color, Lexus_IS.number_of_cylinders))
print("Toyota_Camry is now {0} and only has {1} cylinders".format(Toyota_Camry.color[0], Toyota_Camry.number_of_cylinders))
print("Toyota_Corolla is still {0} and still has {1} cylinders".format(Toyota_Corolla.color, Toyota_Corolla.number_of_cylinders))