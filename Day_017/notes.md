# Day 017

## Topic
(To be updated)

## What I Learned
- 

## Key Notes
-
# Day 17 – Web Development

## What is Web Development?
Web development means creating websites or web applications.
Users open them in a browser.
Python runs on a server behind the scenes.

Python handles:
- Pages
- Forms
- Data
- Requests
- Login pages
- Dashboards

## How Python Fits In
Python does not run in the browser.
Python runs on a server.

Flow:
Browser → Request → Python (Server) → Response

## Step 1 – Flask Basics

### What is Flask?
Flask is:
- A lightweight Python web framework
- Beginner-friendly
- Used for simple and medium websites

### Installing Flask
Flask must be installed once using pip.

### Creating a Flask App
Flask(__name__) creates the web application.
The app variable represents the website.

### Running the App
Running the file starts a local web server.
debug=True enables auto reload and error messages.

## Step 2 – FastAPI Basics

### What is FastAPI?
FastAPI is:
- Very fast
- Modern
- Mostly used for APIs

Flask is used mainly for websites.
FastAPI is used mainly for backend services.

FastAPI returns JSON by default.

## Step 3 – Routing

### What is Routing?
Routing connects a URL path to a Python function.
Each route runs a function when visited.

## Step 4 – Templates

### What are Templates?
Templates are HTML files.
They display pages to users.
They can show Python data.

Flask looks for templates inside a templates folder.

## Step 5 – Request Handling

### What is a Request?
A request happens when a user:
- Opens a page
- Clicks a button
- Submits a form

### GET Requests
GET requests send data through the URL.

### POST Requests
POST requests send data securely through forms.

## Step 6 – Summary
- Web development builds websites
- Flask and FastAPI are Python web tools
- Routing maps URLs to functions
- Templates render HTML pages
- Requests handle user input
- Python controls server behavior
