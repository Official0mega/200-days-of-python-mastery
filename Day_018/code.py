"""
Day 018 Practice
Author: James
"""

# Write your Python code here
# Day 18 – Multithreading Example

import time
import threading

def task():
    print("Task started")
    time.sleep(2)
    print("Task finished")

thread1 = threading.Thread(target=task)
thread2 = threading.Thread(target=task)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("All tasks done")


# Day 18 – Multiprocessing Example

import time
import multiprocessing

def work():
    print("Process working")
    time.sleep(2)

if __name__ == "__main__":
    process1 = multiprocessing.Process(target=work)
    process2 = multiprocessing.Process(target=work)

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    print("All processes finished")


# Day 18 – Async IO Example

import asyncio

async def async_task():
    print("Task started")
    await asyncio.sleep(2)
    print("Task finished")

async def main():
    await asyncio.gather(
        async_task(),
        async_task()
    )

asyncio.run(main())
