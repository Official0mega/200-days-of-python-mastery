"""
Day 020 Practice
Author: James
"""

# Write your Python code here
# Day 20 – Example setup.py

from setuptools import setup, find_packages

setup(
    name="mypackage",
    version="1.0.0",
    packages=find_packages(),
)


# Day 20 – Example requirements.txt content (represented as string)

requirements = """
requests
flask
"""


# Example main module inside mypackage/main.py

def greet(name):
    return f"Hello {name}"


# Example usage after installation

if __name__ == "__main__":
    print(greet("James"))
