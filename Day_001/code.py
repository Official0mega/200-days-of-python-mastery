"""
Day 001 Practice
Author: James
"""

# Write your Python code here
"""
Module 11: File Handling – Core Python
Author: James

This file demonstrates:
- Writing and reading text files
- Appending to files
- Working with CSV files
- Working with JSON files
- Using with open()
- Exception-safe file handling
"""

# -------------------------------
# Writing to a text file
# -------------------------------
with open("example.txt", "w") as file:
    file.write("Hello, world!\n")
    file.write("This is a file created using Python.\n")

# -------------------------------
# Reading from a text file
# -------------------------------
with open("example.txt", "r") as file:
    content = file.read()
    print("File Content:")
    print(content)

# -------------------------------
# Reading line by line
# -------------------------------
with open("example.txt", "r") as file:
    print("Reading line by line:")
    for line in file:
        print(line.strip())

# -------------------------------
# Appending to a file
# -------------------------------
with open("example.txt", "a") as file:
    file.write("New line added without deleting old content.\n")

# -------------------------------
# Working with CSV files
# -------------------------------
import csv

with open("people.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "age", "city"])
    writer.writerow(["Ada", 20, "Lagos"])
    writer.writerow(["James", 25, "Abuja"])

with open("people.csv", "r") as file:
    reader = csv.reader(file)
    print("CSV File Content:")
    for row in reader:
        print(row)

# -------------------------------
# Working with JSON files
# -------------------------------
import json

data = {
    "name": "James",
    "age": 25,
    "city": "Abuja"
}

with open("data.json", "w") as file:
    json.dump(data, file)

with open("data.json", "r") as file:
    loaded_data = json.load(file)
    print("JSON File Content:")
    print(loaded_data)

# -------------------------------
# Exception-safe file handling
# -------------------------------
try:
    with open("missing_file.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("Error: File not found.")
