"""
Day 005 Practice
Author: James
"""

# Write your Python code here
# Day 5 - Core OOP Concepts

# Encapsulation
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def show_balance(self):
        print("Balance:", self.__balance)

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

account = BankAccount(1000)
account.show_balance()

# Inheritance
class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def bark(self):
        print("Dog barks")

dog = Dog()
dog.speak()
dog.bark()

# Polymorphism (Method Overriding)
class Cat(Animal):
    def speak(self):
        print("Meow")

cat = Cat()
cat.speak()

# Method Overloading (simulated)
class Calculator:
    def add(self, a, b=0):
        print(a + b)

calc = Calculator()
calc.add(5)
calc.add(5, 10)

# Abstraction
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def area(self):
        print("Area = side * side")

square = Square()
square.area()
