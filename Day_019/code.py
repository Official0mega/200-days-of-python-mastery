"""
Day 019 Practice
Author: James
"""

# Write your Python code here
# Day 19 – unittest example

# calculator.py
def add(a, b):
    return a + b


# test_calculator.py
import unittest
from calculator import add

class TestCalculator(unittest.TestCase):

    def test_add(self):
        result = add(2, 3)
        self.assertEqual(result, 5)

if __name__ == "__main__":
    unittest.main()


# Day 19 – pytest example

from calculator import add

def test_add():
    assert add(2, 3) == 5


# Day 19 – Mocking example

from unittest.mock import Mock

fake_api = Mock()
fake_api.get_data.return_value = 100

print(fake_api.get_data())


# Day 19 – pdb debugging example

import pdb

def divide(a, b):
    pdb.set_trace()
    return a / b

divide(10, 2)
