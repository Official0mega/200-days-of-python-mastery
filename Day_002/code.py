"""
Day 002 Practice
Author: James
"""

# Write your Python code here
# Day 2 - File Handling Practice

import csv
import json

# Write CSV
with open("people.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "age", "city"])
    writer.writerow(["Ada", 20, "Lagos"])
    writer.writerow(["James", 25, "Abuja"])

# Read CSV
with open("people.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# Write JSON
data = {
    "count": 2,
    "names": ["Ada", "James"]
}

with open("summary.json", "w") as file:
    json.dump(data, file, indent=4)

# Read JSON
with open("summary.json", "r") as file:
    summary = json.load(file)
    print(summary)

# Safe file handling
try:
    with open("missing.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("File not found")
