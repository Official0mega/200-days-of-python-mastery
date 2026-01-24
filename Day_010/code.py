"""
Day 010 Practice
Author: James
"""

# Write your Python code here
# Day 10 – Context Managers

# Using with to manage files
with open("example.txt", "w") as file:
    file.write("Hello World")

with open("example.txt", "r") as file:
    content = file.read()
    print(content)


# Custom Context Manager
class MyContext:
    def __enter__(self):
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting the context")


with MyContext():
    print("Inside the context")


# Handling errors in context manager
class SafeContext:
    def __enter__(self):
        print("Start")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("End")
        if exc_type:
            print("An error happened")
        return True


with SafeContext():
    print(10 / 0)
