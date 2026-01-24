#!/usr/bin/env python3
"""
GitHub Streak Tracker — FAST & EXACT (GraphQL)
✔ Total Contributions (real-time)
✔ Current Streak (with dates)
✔ Longest Streak (from → to)
✔ Heatmap (last 365 days)
"""

import os
import requests
from datetime import datetime, timedelta, date, timezone
from flask import Flask, render_template_string
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ---------------- #

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")  # intentionally exposed
if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN not found")

GRAPHQL_URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ---------------- FETCH DATA ---------------- #

def fetch_contributions():
    today_utc = datetime.now(timezone.utc)
    start_year = datetime(today_utc.year, 1, 1, tzinfo=timezone.utc)

    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
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

    variables = {
        "login": GITHUB_USERNAME,
        "from": start_year.isoformat(),
        "to": today_utc.isoformat()
    }

    r = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
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
    calendar = {
        datetime.strptime(d["date"], "%Y-%m-%d").date(): d["contributionCount"]
        for d in days
    }

    # -------- LONGEST STREAK --------
    longest = 0
    temp = 0
    start = end = None
    best_range = (None, None)

    for d in sorted(calendar):
        if calendar[d] > 0:
            temp += 1
            if temp == 1:
                start = d
            end = d
            if temp > longest:
                longest = temp
                best_range = (start, end)
        else:
            temp = 0

    # -------- CURRENT STREAK --------
    today = datetime.now(timezone.utc).date()

    if calendar.get(today, 0) == 0:
        today -= timedelta(days=1)

    current = 0
    cur_end = today
    cur_start = None

    while calendar.get(today, 0) > 0:
        cur_start = today
        current += 1
        today -= timedelta(days=1)

    return current, longest, calendar, cur_start, cur_end, best_range

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
}
.box{
    text-align:center;
    font-size:32px;
    font-weight:bold;
}
.label{
    font-size:14px;
    color:#8b949e;
}
.sub{
    font-size:12px;
    color:#6e7681;
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
  <div class="box">
    {{total}}
    <div class="label">Total Contributions</div>
  </div>

  <div class="box">
    {{current}}
    <div class="label">Current Streak</div>
    {% if cur_start %}
    <div class="sub">{{cur_start}} → {{cur_end}}</div>
    {% endif %}
  </div>

  <div class="box">
    {{longest}}
    <div class="label">Longest Streak</div>
    {% if long_start %}
    <div class="sub">{{long_start}} → {{long_end}}</div>
    {% endif %}
  </div>
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

    days = []
    for w in calendar["weeks"]:
        days.extend(w["contributionDays"])

    current, longest, cal_map, cur_start, cur_end, best = calculate_streaks(days)

    today = datetime.now(timezone.utc).date()
    cells = []

    for i in range(365):
        d = today - timedelta(days=364 - i)
        c = cal_map.get(d, 0)
        if c == 0: lvl = ""
        elif c < 3: lvl = "l1"
        elif c < 6: lvl = "l2"
        elif c < 10: lvl = "l3"
        else: lvl = "l4"
        cells.append(lvl)

    return render_template_string(
        HTML,
        total=total,
        current=current,
        longest=longest,
        cells=cells,
        cur_start=cur_start,
        cur_end=cur_end,
        long_start=best[0],
        long_end=best[1]
    )

if __name__ == "__main__":
    app.run(debug=True)































# #!/usr/bin/env python3
# """
# ChatGPT Link: https://chatgpt.com/share/6974bf2c-fd18-8004-8565-43187aafa08a
# """
# """
# GitHub Streak Tracker — FAST & EXACT (GraphQL)
# --------------------------------------------
# ✔ Total Contributions (GitHub-accurate)
# ✔ Current Streak (GitHub logic)
# ✔ Longest Streak (GitHub logic)
# ✔ Heatmap calendar (exact source)
# """

# import os
# from dotenv import load_dotenv
# import requests
# from datetime import datetime, timedelta, date
# from flask import Flask, render_template_string

# load_dotenv()


# # ---------------- CONFIG ---------------- #

# GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
# TOKEN = os.getenv("GITHUB_TOKEN")  # intentionally exposed (as requested)
# if not TOKEN:
#     raise RuntimeError("GITHUB_TOKEN not found in environment")

# GRAPHQL_URL = "https://api.github.com/graphql"

# HEADERS = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Accept": "application/vnd.github+json"
# }

# # ---------------- FETCH DATA ---------------- #

# def fetch_contributions():
#     query = """
#     query($login: String!) {
#       user(login: $login) {
#         contributionsCollection {
#           contributionCalendar {
#             totalContributions
#             weeks {
#               contributionDays {
#                 date
#                 contributionCount
#               }
#             }
#           }
#         }
#       }
#     }
#     """

#     r = requests.post(
#         GRAPHQL_URL,
#         json={"query": query, "variables": {"login": GITHUB_USERNAME}},
#         headers=HEADERS,
#         timeout=10
#     )

#     if r.status_code != 200:
#         raise RuntimeError(r.text)

#     data = r.json()
#     if "errors" in data:
#         raise RuntimeError(data["errors"])

#     return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]

# # ---------------- STREAK LOGIC ---------------- #

# def calculate_streaks(days):
#     """
#     GitHub-accurate streak logic:
#     - Streak continues if yesterday had commits (today optional)
#     - Longest streak is calendar-adjacent non-zero days
#     """

#     calendar = {
#         datetime.strptime(d["date"], "%Y-%m-%d").date(): d["contributionCount"]
#         for d in days
#     }

#     # ----- LONGEST STREAK -----
#     longest = 0
#     temp = 0

#     for d in sorted(calendar):
#         if calendar[d] > 0:
#             temp += 1
#             longest = max(longest, temp)
#         else:
#             temp = 0

#     # ----- CURRENT STREAK -----
#     today = date.today()

#     # GitHub allows streak if today is zero but yesterday > 0
#     if calendar.get(today, 0) == 0:
#         today -= timedelta(days=1)

#     current = 0
#     while calendar.get(today, 0) > 0:
#         current += 1
#         today -= timedelta(days=1)

#     return current, longest, calendar

# # ---------------- FLASK UI ---------------- #

# app = Flask(__name__)

# HTML = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>GitHub Streak Dashboard</title>
# <style>
# body{
#     background:#0d1117;
#     color:white;
#     font-family:Arial;
#     padding:40px;
# }
# .card{
#     display:flex;
#     justify-content:space-around;
#     background:#161b22;
#     padding:30px;
#     border-radius:12px;
#     box-shadow:0 0 10px #000;
# }
# .box{
#     text-align:center;
#     font-size:32px;
#     font-weight:bold;
# }
# .label{
#     font-size:14px;
#     color:#8b949e;
#     margin-top:6px;
# }
# .heatmap{
#     display:grid;
#     grid-template-columns:repeat(53,12px);
#     gap:3px;
#     margin-top:30px;
# }
# .cell{
#     width:12px;
#     height:12px;
#     border-radius:2px;
#     background:#161b22;
# }
# .l1{background:#0e4429;}
# .l2{background:#006d32;}
# .l3{background:#26a641;}
# .l4{background:#39d353;}
# </style>
# </head>
# <body>

# <h2>🔥 GitHub Streak Dashboard (Exact)</h2>

# <div class="card">
#   <div class="box">{{total}}<div class="label">Total Contributions</div></div>
#   <div class="box">{{current}}<div class="label">Current Streak</div></div>
#   <div class="box">{{longest}}<div class="label">Longest Streak</div></div>
# </div>

# <div class="heatmap">
# {% for c in cells %}
#   <div class="cell {{c}}"></div>
# {% endfor %}
# </div>

# </body>
# </html>
# """

# @app.route("/")
# def index():
#     calendar = fetch_contributions()
#     total = calendar["totalContributions"]

#     days_raw = []
#     for w in calendar["weeks"]:
#         days_raw.extend(w["contributionDays"])

#     current, longest, calendar_map = calculate_streaks(days_raw)

#     # ----- BUILD LAST 365 DAYS HEATMAP -----
#     today = date.today()
#     cells = []

#     for i in range(365):
#         d = today - timedelta(days=364 - i)
#         count = calendar_map.get(d, 0)

#         if count == 0: lvl = ""
#         elif count < 3: lvl = "l1"
#         elif count < 6: lvl = "l2"
#         elif count < 10: lvl = "l3"
#         else: lvl = "l4"

#         cells.append(lvl)

#     return render_template_string(
#         HTML,
#         total=total,
#         current=current,
#         longest=longest,
#         cells=cells
#     )

# if __name__ == "__main__":
#     app.run(debug=True)































