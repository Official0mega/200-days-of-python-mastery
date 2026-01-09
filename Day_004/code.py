"""
Day 004 Practice
Author: James
"""

# Write your Python code here
# Day 4 - Introduction to OOP

# Class and Object
class Car:
    pass

my_car = Car()

# __init__ constructor
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person1 = Person("James", 25)

# Instance vs Class Variables
class Dog:
    species = "Animal"  # class variable

    def __init__(self, name):
        self.name = name  # instance variable

dog1 = Dog("Bingo")
dog2 = Dog("Max")

print(dog1.name)
print(dog2.name)
print(dog1.species)
print(dog2.species)

# Methods and self
class Student:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello, my name is", self.name)

student1 = Student("Ayo")
student1.greet()
