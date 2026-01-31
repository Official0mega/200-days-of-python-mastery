# Day 015

## Topic
(To be updated)

## What I Learned
- 

## Key Notes
-
# Day 15 – Working with APIs

## What is an API?
An API is a messenger between your Python program and another app or website.

## How an API Works
1. Python sends a request
2. The server receives it
3. The server sends back data
4. Python reads the data

## Real-Life Uses of APIs
- Weather apps
- Payment systems
- Login systems
- Chat applications

## Step 1 – requests Module
The requests module allows Python to:
- Send requests to the internet
- Receive data from servers
- Communicate with APIs

### Installation
pip install requests  
(Only done once)

### Important Notes
- Always check response status codes
- Do not trust data without checking status

### Common Status Codes
- 200 → Success
- 401 → Unauthorized
- 404 → Not Found

## Step 2 – JSON Handling
JSON:
- Is text-based data
- Looks like Python dictionaries
- Is the standard format used by APIs

### Why JSON is Important
- Easy to read
- Easy to send
- Easy to store
- Supported by almost all APIs

## Step 3 – Authentication and Headers
Authentication is how APIs verify identity.

APIs may require:
- API keys
- Tokens
- Login credentials

Headers send extra information such as:
- Authorization tokens
- Content type
- Accepted data format

## Common Beginner Mistakes
- Forgetting headers
- Using wrong API keys
- Not converting response to JSON
- Using the wrong request method

## Summary
- APIs connect Python to external services
- requests handles HTTP communication
- JSON is the main data format
- Headers carry authentication and metadata
- Authentication protects API access
