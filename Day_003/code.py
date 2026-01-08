"""
Day 003 Practice
Author: James
"""

# Write your Python code here
# Day 3 - Error and Exception Handling

# Basic try / except
try:
    x = 10 / 0
except:
    print("An error occurred")

# Catching a specific error
try:
    number = int("hello")
except ValueError:
    print("Invalid number")

# try + except + else
try:
    value = int("20")
except ValueError:
    print("Conversion failed")
else:
    print("Conversion successful:", value)

# finally example
try:
    file = open("data.txt", "r")
except FileNotFoundError:
    print("File not found")
finally:
    print("Cleanup complete")

# Raising an exception
age = -5
if age < 0:
    raise ValueError("Age cannot be negative")

# Custom exception
class LowBalanceError(Exception):
    pass

balance = 500

def withdraw(amount):
    if amount > balance:
        raise LowBalanceError("Not enough balance")
    print("Withdrawal successful")

try:
    withdraw(1000)
except LowBalanceError as e:
    print(e)
