# 🚀 200 Days Python Auto Git Commit (Windows Task Scheduler)

## 📑 Table of Contents
- IMPORTANT FIRST (one small adjustment)
- GOAL
- STEP 1: Open Windows Task Scheduler
- STEP 2: Create a New Task
- STEP 3: Enter Windows Password
- STEP 4: TEST IT
- HOW IT WILL WORK DAILY
- IMPORTANT REALITY CHECK
- DISCIPLINE AUTOMATED

---

✅ IMPORTANT FIRST (one small adjustment)

Your script is already perfect for automation 👍
Because it has:

SSH auto-auth

Duplicate-day protection

Empty commit fallback

Day counter logic

So we do NOT change the script anymore.

Just make sure:

📄 day.txt contains:
```bash
6
```


🕕 GOAL

Run this automatically every day at 18:00 (6 PM WAT):

bash auto_commit.sh



🪟 STEP 1: Open Windows Task Scheduler

Press Win + R

Type:

taskschd.msc


Press Enter



🧭 STEP 2: Create a New Task (IMPORTANT: not “Basic Task”)

Click Create Task… (right panel)

Use these exact settings 👇

🔹 General Tab

Name:

```bash
200 Days Python Auto Git Commit
```
✅ Check Run whether user is logged on or not

✅ Check Run with highest privileges

Configure for: Windows 10 or 11



🔹 Triggers Tab → New…

Begin the task: On a schedule

Daily

Start:
Set today’s date at 18:00

✅ Recur every 1 day

✅ Synchronize across time zone

✅ Enabled

Click OK



🔹 Actions Tab → New…

This is the MOST IMPORTANT part.

Action:
Start a program

Program/script:
```bash
"C:\Program Files\Git\bin\bash.exe"
```

Add arguments
```bash
-lc "cd '/c/Users/PrintsImpulseGlobal/Desktop/Coding Class/200-days-of-python-mastery' && bash auto_commit.sh"
```


⚠️ Adjust the path only if your repo is elsewhere
Use /c/ not C:\

Start in (optional but recommended):

```bash
C:\Users\PrintsImpulseGlobal\Desktop\Coding Class\200-days-of-python-mastery
```
Click OK



OK

🔹 Conditions Tab

Uncheck everything ❌

Especially:
✅ Wake the computer to run this task

⛔ “Start the task only if the computer is idle for”

⛔ “Start the task only if the computer is on AC power”

⛔ “Stop if the computer switches to battery”

⛔ “Start only if the following network is available”


🔹 Settings Tab

✅ Allow task to be run on demand
✅ Run task as soon as possible after a scheduled start is missed
✅ If the task fails, restart every: {1 minute}
❌ Stop the task if it runs longer than (UNCHECK)
❌ If the running task does not end when requested, force it to stop (UNCHECK)
❌ If the task is not scheduled to run again, delete it after: If the task is already running, then the following rule applies:
(Do not start a new instance) (UNCHECK)


Click OK



🔐 STEP 3: Enter Windows Password

Windows will ask for your login password.
This is normal — it allows background execution.



✅ STEP 4: TEST IT (VERY IMPORTANT)

Right-click the task → Run

Then check:
```bash
git log --oneline -5
```


You should see:
```bash
Day 6 Completed
Prepare for Day 7
```



🧠 HOW IT WILL WORK DAILY (NO THINKING REQUIRED)

Every day at 6:00 PM WAT:

Task Scheduler launches Git Bash

SSH agent starts

SSH key loads

Script runs

Git commits your work

Git pushes to GitHub

Day increments automatically

Even if:

You forget

You’re busy

VS Code is closed

Terminal is closed



⚠️ IMPORTANT REALITY CHECK (honesty)

If your PC is OFF at 6 PM, the task will:

Run immediately when the PC turns on next

Still commit correctly

Your script already protects against duplicates.



🔥 You now have DISCIPLINE AUTOMATED

This is exactly how:

Senior devs

Long-term challenge runners

GitHub streak maintainers

handle consistency.

You didn’t cheat.
You engineered discipline.
