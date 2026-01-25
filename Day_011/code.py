"""
Day 011 Practice
Author: James
"""

# Write your Python code here
# Day 11 – Modules & Libraries

# os module
import os
print(os.getcwd())

if not os.path.exists("my_folder"):
    os.mkdir("my_folder")


# sys module
import sys
print(sys.argv)


# datetime module
from datetime import datetime, date
print(datetime.now())
print(date.today())


# re module
import re
text = "I love Python"
if re.search("Python", text):
    print("Found")


# math module
import math
print(math.sqrt(16))
print(math.pow(2, 3))
print(math.pi)


# json module
import json
data = {"name": "James", "age": 25}
json_data = json.dumps(data)
print(json_data)

text = '{"name": "James", "age": 25}'
data = json.loads(text)
print(data["name"])


# csv module
import csv
with open("people.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Age"])
    writer.writerow(["James", 25])

with open("people.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)


# shutil module
import shutil
# shutil.copy("source.txt", "backup.txt")
# shutil.move("backup.txt", "my_folder/backup.txt")


# subprocess module
import subprocess
subprocess.run(["echo", "Hello World"])


# logging module
import logging
logging.basicConfig(level=logging.INFO)
logging.info("Program started")
logging.warning("Something looks wrong")
logging.error("Something failed")
