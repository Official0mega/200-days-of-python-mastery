# Day 018

## Topic
(To be updated)

## What I Learned
- 

## Key Notes
-
# Day 18 – Concurrency and Parallelism

## What Does This Mean?
Normally, Python runs one task at a time.
Concurrency and Parallelism allow:
- Doing many tasks at the same time
- Or switching between tasks very fast

This makes programs faster.

## Simple Example
One pot cooking → slow
Many pots cooking → fast

That is concurrency.

## Step 1 – Multithreading (threading module)

### What is Multithreading?
Multithreading means:
- One Python program
- Multiple threads (small workers)
- Tasks run almost together

All threads:
- Share the same memory
- Share the same data

### Best Use Cases
- Waiting tasks
- Downloads
- File reading
- API calls

### How It Works
Threads run tasks at the same time while sharing memory.

## Step 2 – Multiprocessing (multiprocessing module)

### What is Multiprocessing?
Multiprocessing means:
- Using multiple CPU cores
- Each task is a separate process
- Faster for heavy work

Key points:
- Each process has its own memory
- No memory sharing
- More powerful than threading

### Best Use Cases
- Heavy calculations
- Data processing
- CPU-intensive work

### Threading vs Multiprocessing
Threading:
- One CPU
- Shared memory
- Light tasks

Multiprocessing:
- Many CPUs
- Separate memory
- Heavy tasks

### Why __name__ == "__main__"?
- Prevents infinite process creation
- Prevents crashes
- Required on Windows
- Keeps multiprocessing safe

## Step 3 – Async IO (async, await, asyncio)

### What is Async IO?
Async means:
- Do not block
- Do not wait doing nothing
- While waiting, do other work

Async uses:
- No threads
- No processes
- Smart waiting

### Best Use Cases
- Websites
- APIs
- Network requests

### Keywords Explained
async:
- Defines a function that can pause

await:
- Wait without blocking

asyncio:
- Manages async tasks

## Step 4 – Summary
- Threading handles waiting tasks
- Multiprocessing handles heavy CPU tasks
- Async handles non-blocking waiting
- Each method solves different problems

## When to Use What?
- API calls → Async
- Downloads → Threading
- Heavy math → Multiprocessing
- Websites → Async
