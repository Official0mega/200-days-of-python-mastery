"""
Day 013 Practice
Author: James
"""

# Write your Python code here
# Day 13 – Regular Expressions (re)

import re

# match()
text = "Python is fun"
result = re.match("Python", text)
print(result)

# search()
result = re.search("fun", text)
print(result)

# findall()
text = "I have 2 apples and 3 oranges"
numbers = re.findall(r"\d", text)
print(numbers)

# sub()
text = "I like cats"
new_text = re.sub("cats", "dogs", text)
print(new_text)

# Meta-characters
text = "My number is 08123456789"
result = re.search(r"\d+", text)
print(result.group())

# Groups
text = "Email: test@gmail.com"
pattern = r"(\w+)@(\w+).(\w+)"
match = re.search(pattern, text)

print(match.group(1))
print(match.group(2))
print(match.group(3))
