# - Class Animal  
# - Classes for each animal  
# - Methods that model the behaviors of each animal ndd body fetures
# Group each animaalss into categories like birds, reptiles, 
class Animal:
    def __init__(self, name, animal_class, sound):
        self.animal_class = animal_class
        self.name = name
        self.sound = sound
    def __str__(self):
        return("I am  an Animal and I fly")
    def make_a_sound(self):
        print(f"{self.sound} {self.sound}")

class Bird(Animal):
    def __init__(self, name, can_fly, sound):
        Animal.__init__(self, name, sound)
        self.can_fly = can_fly
        self.covering = "feathers"
        self.sound = sound
    def __str__(self):
        return("I am  bird and I fly")
    

class Fish(Animal):
    def __init__(self, habitat):
        self.no_of_legs = 2
        self.covering = "scales"
        self.habitat = habitat

class Reptiles(Animal):
    def __init__(self, habitat, no_of_legs):
        self.no_of_legs = 2
        self.covering = "scales"

chicken = Animal("chicken", Bird, "cackle")
chicken.make_a_sound()

