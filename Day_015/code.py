"""
Day 015 Practice
Author: James
"""

# Write your Python code here
# Day 15 – Working with APIs

import requests

# Simple GET request
url = "https://api.github.com"
response = requests.get(url)

print(response.status_code)
print(response.text)

# Convert response to JSON
data = response.json()
print(data)

# Access JSON data like a dictionary
print(data["current_user_url"])
                                                           
# Loop through JSON data
for key, value in data.items():
    print(key, ":", value)

# Sending headers with authentication
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

responszZZZZS                                                                                                                                                                                                                                                                                                                                                                                        e = requests.get("https://api.example.com/data", headers=headers)
print(response.status_code)

# POST request with JSON data
post_url = "https://api.example.com/create"

payload = {
    "name": "James",
    "age": 25
}

response = requests.post(post_url, json=payload)
print(response.status_code)
