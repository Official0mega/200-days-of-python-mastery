# Day 016

## Topic
(To be updated)

## What I Learned
- 

## Key Notes
-
# Day 16 – Databases

## What is a Database?
A database is a place where data is stored permanently.
Data remains saved even after the program closes.

## Variables vs Database
Variables:
- Exist only while the program runs
- Lost when the program stops

Database:
- Saves data permanently
- Can be reused later

## Real-Life Example
A database is like an Excel sheet:
- Smarter
- Faster
- Safer

## Step 1 – SQLite3 Basics

### What is SQLite?
SQLite is:
- A lightweight database
- Built into Python
- No installation required
- Stored in a single file

### Import sqlite3
Importing sqlite3 allows Python to work with SQLite databases.

### Connect to a Database
Connecting creates the database file if it does not exist.

### Cursor
A cursor sends commands to the database.
Without it, Python cannot execute SQL commands.

### Creating a Table
Tables store data in rows and columns.
IF NOT EXISTS prevents errors.
commit() saves changes.

## Step 2 – CRUD Operations
CRUD means:
- Create
- Read
- Update
- Delete

These are the four basic database actions.

### CREATE
Adds new data to the database.

### READ
Fetches stored data.

### UPDATE
Changes existing data.

### DELETE
Removes data from the database.

### Closing the Connection
Always close the database when finished.

## Step 3 – ORMs (SQLAlchemy)

### What is an ORM?
An ORM lets you write Python code instead of SQL.
It automatically converts Python to SQL.

### Why Use ORMs?
- Cleaner syntax
- Fewer errors
- Used in real applications

### What is SQLAlchemy?
SQLAlchemy is:
- A popular ORM
- Professional and reliable
- Safer than raw SQL

## Step 4 – Summary
- Databases store data permanently
- SQLite is built into Python
- CRUD controls database actions
- SQLAlchemy replaces SQL with Python
- ORMs are cleaner and safer
