# Day 001
Today_5th_January_2026
## Topic
Day 1 Completed

## What I Learned
- 

## Key Notes
-
# Module 11 – File Handling (Core Python)

File handling allows a Python program to **save data to files** and **read data from files**.

Think of a file as a **notebook on your computer**:
- Python can open it
- Read what is inside
- Write new content
- Close it safely

This module focuses on **safe and practical file operations**.

---

## 🔸 Topics Covered
- Reading and writing text files
- Working with CSV and JSON files
- Using the `with open()` context manager
- Exception-safe file operations

---

## 📝 Step 1 – Reading and Writing Text Files

### What is a Text File?
A text file contains normal readable text, such as:
- `.txt`
- `.py`
- `.log`

---

### ✍️ Writing to a Text File
Steps:
1. Open the file in **write mode**
2. Write text into it
3. Close the file

Important notes:
- `"w"` creates the file if it doesn’t exist
- `"w"` deletes old content if the file already exists
- Always close files after writing

---

### 📖 Reading from a Text File
Steps:
1. Open the file in **read mode**
2. Read the content
3. Close the file

You can:
- Read the entire file at once
- Read line by line using a loop

---

### ➕ Appending to a File
- Append mode (`"a"`) adds new content **without deleting existing data**

---

### 📌 File Modes Summary
- `"r"` → read
- `"w"` → write (overwrite)
- `"a"` → append
- `"r+"` → read and write

---

## 📊 Step 2 – Working with CSV and JSON Files

### What is a CSV File?
CSV (Comma Separated Values) files store data in **table form**.

Example:
```bash
name,age,city
Ada,20,Lagos
James,25,Abuja
```


- Commonly used for data storage and spreadsheets
- Python uses the `csv` module to work with CSV files

---

### What is a JSON File?
- JSON stores data as **key-value pairs**
- Very common in APIs and real-world applications
- Python uses the `json` module

---

## 🔐 Using `with open()` (Best Practice)

The `with open()` statement:
- Automatically closes the file
- Prevents memory leaks
- Is the **recommended way** to work with files

---

## ⚠️ Exception-Safe File Handling
- Errors can occur if files don’t exist or permissions are denied
- `try` and `except` help prevent program crashes
- Always handle file errors gracefully

---

## ✅ Summary
In this module, we learned how to:
- Read and write files safely
- Work with CSV and JSON data
- Use `with open()` properly
- Handle file-related errors professionally

File handling is a **core skill** for real-world Python programs.

