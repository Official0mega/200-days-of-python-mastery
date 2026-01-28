"""
Day 012 Practice
Author: James
"""

# Write your Python code here
# Day 12 – List Comprehensions

# List comprehension
numbers = [x for x in range(5)]
print(numbers)

# List comprehension with condition
even_numbers = [x for x in range(10) if x % 2 == 0]
print(even_numbers)

# Dictionary comprehension
squares = {x: x * x for x in range(5)}
print(squares)

# Set comprehension
unique_numbers = {x for x in [1, 2, 2, 3, 3, 4]}
print(unique_numbers)

# Nested list comprehension
pairs = [(x, y) for x in range(3) for y in range(2)]
print(pairs)

# Nested comprehension example (matrix)
matrix = [[x for x in range(3)] for y in range(3)]
print(matrix)
