"""
Day 006 Practice
Author: James
"""

# Write your Python code here
# Day 6 - Magic (Dunder) Methods

# __str__ and __repr__
class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Person name is {self.name}"

    def __repr__(self):
        return f"Person('{self.name}')"

p = Person("James")
print(p)

# __len__, __getitem__, __setitem__
class Team:
    def __init__(self, members):
        self.members = members

    def __len__(self):
        return len(self.members)

    def __getitem__(self, index):
        return self.members[index]

    def __setitem__(self, index, value):
        self.members[index] = value

team = Team(["Ayo", "Tunde", "Zainab"])
print(len(team))
print(team[1])
team[1] = "Sadiq"
print(team.members)

# __eq__ and __lt__
class Student:
    def __init__(self, score):
        self.score = score

    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score

print(Student(80) == Student(80))
print(Student(70) < Student(90))

# __add__ and operator overloading
class Wallet:
    def __init__(self, money):
        self.money = money

    def __add__(self, other):
        return self.money + other.money

w1 = Wallet(500)
w2 = Wallet(700)
print(w1 + w2)
