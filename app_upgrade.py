#!/usr/bin/env python3
"""
ChatGPT Link: https://chatgpt.com/share/6974bf2c-fd18-8004-8565-43187aafa08a
"""
"""
GitHub Streak Tracker — FAST & EXACT (GraphQL)
--------------------------------------------
✔ Total Contributions (GitHub-accurate)
✔ Current Streak (GitHub logic)
✔ Longest Streak (GitHub logic)
✔ Heatmap calendar (exact source)
"""

import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta, date
from flask import Flask, render_template_string

load_dotenv()


# ---------------- CONFIG ---------------- #

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")  # intentionally exposed (as requested)
if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN not found in environment")

GRAPHQL_URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ---------------- FETCH DATA ---------------- #

def fetch_contributions():
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    r = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": {"login": GITHUB_USERNAME}},
        headers=HEADERS,
        timeout=10
    )

    if r.status_code != 200:
        raise RuntimeError(r.text)

    data = r.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])

    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]

# ---------------- STREAK LOGIC ---------------- #

def calculate_streaks(days):
    """
    GitHub-accurate streak logic:
    - Streak continues if yesterday had commits (today optional)
    - Longest streak is calendar-adjacent non-zero days
    """

    calendar = {
        datetime.strptime(d["date"], "%Y-%m-%d").date(): d["contributionCount"]
        for d in days
    }

    # ----- LONGEST STREAK -----
    longest = 0
    temp = 0

    for d in sorted(calendar):
        if calendar[d] > 0:
            temp += 1
            longest = max(longest, temp)
        else:
            temp = 0

    # ----- CURRENT STREAK -----
    today = date.today()

    # GitHub allows streak if today is zero but yesterday > 0
    if calendar.get(today, 0) == 0:
        today -= timedelta(days=1)

    current = 0
    while calendar.get(today, 0) > 0:
        current += 1
        today -= timedelta(days=1)

    return current, longest, calendar

# ---------------- FLASK UI ---------------- #

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>GitHub Streak Dashboard</title>
<style>
body{
    background:#0d1117;
    color:white;
    font-family:Arial;
    padding:40px;
}
.card{
    display:flex;
    justify-content:space-around;
    background:#161b22;
    padding:30px;
    border-radius:12px;
    box-shadow:0 0 10px #000;
}
.box{
    text-align:center;
    font-size:32px;
    font-weight:bold;
}
.label{
    font-size:14px;
    color:#8b949e;
    margin-top:6px;
}
.heatmap{
    display:grid;
    grid-template-columns:repeat(53,12px);
    gap:3px;
    margin-top:30px;
}
.cell{
    width:12px;
    height:12px;
    border-radius:2px;
    background:#161b22;
}
.l1{background:#0e4429;}
.l2{background:#006d32;}
.l3{background:#26a641;}
.l4{background:#39d353;}
</style>
</head>
<body>

<h2>🔥 GitHub Streak Dashboard (Exact)</h2>

<div class="card">
  <div class="box">{{total}}<div class="label">Total Contributions</div></div>
  <div class="box">{{current}}<div class="label">Current Streak</div></div>
  <div class="box">{{longest}}<div class="label">Longest Streak</div></div>
</div>

<div class="heatmap">
{% for c in cells %}
  <div class="cell {{c}}"></div>
{% endfor %}
</div>

</body>
</html>
"""

@app.route("/")
def index():
    calendar = fetch_contributions()
    total = calendar["totalContributions"]

    days_raw = []
    for w in calendar["weeks"]:
        days_raw.extend(w["contributionDays"])

    current, longest, calendar_map = calculate_streaks(days_raw)

    # ----- BUILD LAST 365 DAYS HEATMAP -----
    today = date.today()
    cells = []

    for i in range(365):
        d = today - timedelta(days=364 - i)
        count = calendar_map.get(d, 0)

        if count == 0: lvl = ""
        elif count < 3: lvl = "l1"
        elif count < 6: lvl = "l2"
        elif count < 10: lvl = "l3"
        else: lvl = "l4"

        cells.append(lvl)

    return render_template_string(
        HTML,
        total=total,
        current=current,
        longest=longest,
        cells=cells
    )

if __name__ == "__main__":
    app.run(debug=True)































