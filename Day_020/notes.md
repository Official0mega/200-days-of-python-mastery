# Day 020

## Topic
(To be updated)

## What I Learned
- 

## Key Notes
-
# Day 20 – Packaging and Distribution

## What is Packaging and Distribution?

Packaging means:
- Turning your Python code into something installable

Distribution means:
- Sharing your code with others

Simple idea:
- Code = product
- Packaging = container
- Distribution = sharing

## Step 1 – setup.py

### What is setup.py?
setup.py:
- Defines project name
- Defines version
- Defines included packages

It acts as the project identity file.

### Basic Project Structure
myproject/
- mypackage/
  - __init__.py
  - main.py
- setup.py
- requirements.txt

### Important setup() Fields
- name → project name
- version → project version
- packages → includes Python files

## Step 2 – requirements.txt

### What is requirements.txt?
requirements.txt:
- Lists external libraries needed by the project

### Why it matters
- Installs all dependencies at once
- Prevents missing libraries
- Keeps environments consistent

## Step 3 – Building a Package

### What does building mean?
Building means:
- Creating installable files for pip

After building:
- dist/ folder is created
- Contains .tar.gz file
- Contains .whl file

These files can be installed.

### Installing Locally
pip install .
- Installs the package from the current folder
- Allows importing like a normal library

## Step 4 – Versioning

### What is Versioning?
Versioning gives your project a number.

Format:
MAJOR.MINOR.PATCH

### Meaning of Numbers
- MAJOR → big breaking change
- MINOR → new feature
- PATCH → bug fix

## Step 5 – Publishing

### What is Publishing?
Publishing means:
- Uploading your package online

After publishing:
- Anyone can install it using pip

## Step 6 – Summary
- Packaging prepares code for installation
- Distribution shares the package
- setup.py defines project information
- requirements.txt lists dependencies
- pip installs packages
- Versioning tracks updates
- Publishing makes package public
