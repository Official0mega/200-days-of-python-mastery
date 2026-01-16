"""
Day 008 Practice
Author: James
"""

# Write your Python code here
# Day 8 - Iterators and Generators

# iter() and next()
numbers = [10, 20, 30]
iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))

# Custom Iterator
class CountUp:
    def __init__(self, max_number):
        self.max = max_number
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.max:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

counter = CountUp(3)
for number in counter:
    print(number)

# Generator using yield
def count_up(max_number):
    current = 1
    while current <= max_number:
        yield current
        current += 1

for num in count_up(3):
    print(num)

# Generator expression
numbers = (x for x in range(5))
print(next(numbers))
print(next(numbers))
