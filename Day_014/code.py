"""
Day 014 Practice
Author: James
"""

# Write your Python code here
# Day 14 – Functional Programming

# map()
numbers = [1, 2, 3, 4]

def double(x):
    return x * 2

result = map(double, numbers)
print(list(result))

# filter()
numbers = [1, 2, 3, 4, 5, 6]

def is_even(x):
    return x % 2 == 0

result = filter(is_even, numbers)
print(list(result))

# reduce()
from functools import reduce

numbers = [1, 2, 3, 4]

def add(a, b):
    return a + b

result = reduce(add, numbers)
print(result)

# Higher-order function
def greet(func):
    func()

def say_hello():
    print("Hello!")

greet(say_hello)

# Closure
def outer(name):
    def inner():
        print("Hello", name)
    return inner

my_func = outer("James")
my_func()
