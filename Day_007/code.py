"""
Day 007 Practice
Author: James
"""

# Write your Python code here
# Day 7 - Class Relationships

# Composition
class Engine:
    def start(self):
        print("Engine started")

class Car:
    def __init__(self):
        self.engine = Engine()

    def drive(self):
        self.engine.start()
        print("Car is moving")

car = Car()
car.drive()

# Aggregation
class Student:
    def __init__(self, name):
        self.name = name

class Classroom:
    def __init__(self, students):
        self.students = students

s1 = Student("Ayo")
s2 = Student("Zainab")
room = Classroom([s1, s2])

# Static Method
class MathTools:
    @staticmethod
    def add(a, b):
        return a + b

print(MathTools.add(5, 3))

# Class Method
class Person:
    count = 0

    def __init__(self, name):
        self.name = name
        Person.count += 1

    @classmethod
    def total_people(cls):
        return cls.count

p1 = Person("Ayo")
p2 = Person("Zainab")
print(Person.total_people())

# Property Decorator
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273:
            print("Too cold!")
        else:
            self._celsius = value

temp = Temperature(20)
temp.celsius = -300
temp.celsius = 30
print(temp.celsius)
