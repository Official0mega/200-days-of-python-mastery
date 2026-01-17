"""
Day 009 Practice
Author: James
"""

# Write your Python code here
# Day 9 – Decorators

# Function Decorator
def my_decorator(func):
    def wrapper():
        print("Before the function runs")
        func()
        print("After the function runs")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()


# Chaining Decorators
def decorator_one(func):
    def wrapper():
        print("Decorator One - Before")
        func()
        print("Decorator One - After")
    return wrapper

def decorator_two(func):
    def wrapper():
        print("Decorator Two - Before")
        func()
        print("Decorator Two - After")
    return wrapper

@decorator_one
@decorator_two
def greet():
    print("Hello!")

greet()


# Class Decorator
def add_message(cls):
    cls.message = "Welcome!"
    return cls

@add_message
class User:
    pass

u = User()
print(u.message)
