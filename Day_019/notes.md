# Day 019

## Topic
(To be updated)

## What I Learned
- 

## Key Notes
-
# Day 19 – Testing & Debugging

## What is Testing and Debugging?
Testing means:
- Checking if your code works as expected

Debugging means:
- Finding errors
- Fixing errors

Easy way to remember:
- Testing = exam
- Debugging = correcting mistakes

You test first.
If it fails → you debug.

## Step 1 – unittest

### What is unittest?
unittest is:
- Built into Python
- Used to test functions
- Works like school tests

How it works:
- Write a function
- Write a test
- Python checks the result

### How unittest Works
- Tests run automatically
- Pass if result is correct
- Fail if result is wrong

## Step 2 – pytest

### What is pytest?
pytest is:
- Easier than unittest
- Less code
- Very popular

Key points:
- No classes needed
- Simple test functions
- Uses assert

### Why pytest?
- Cleaner syntax
- Faster writing
- Easy to read

## Step 3 – Mocking

### What is Mocking?
Mocking means:
- Using fake objects instead of real ones

Why mocking is useful:
- No internet needed
- No database needed
- Faster tests

Examples of mocked things:
- APIs
- Databases
- User input

## Step 4 – Test Coverage

### What is Test Coverage?
Test coverage shows:
- How much of your code is tested

Example:
- 100 lines total
- 80 lines tested
- Coverage = 80%

Why coverage matters:
- Shows untested code
- Helps improve test quality

## Step 5 – Debugging with pdb

### What is pdb?
pdb is:
- Python debugger
- Pauses code execution
- Lets you inspect values

What pdb allows:
- Step through code
- Check variable values
- Find where errors happen

### Common pdb Commands
- n → next line
- c → continue
- q → quit
- p x → print variable x

## Step 6 – Summary
- Testing checks correctness
- Debugging fixes errors
- unittest is built-in
- pytest is simpler
- Mocking uses fake data
- Coverage shows tested lines
- pdb helps debug step by step
