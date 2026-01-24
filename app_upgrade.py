
#!/usr/bin/env python3
"""
GitHub Streak Dashboard — EXACT (Matches GitHub)
"""

import os
import requests
from datetime import datetime, timedelta, date, timezone
from flask import Flask, render_template_string
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ---------------- #

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_USERNAME or not TOKEN:
    raise RuntimeError("GITHUB_USERNAME or GITHUB_TOKEN missing")

GRAPHQL_URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ---------------- HELPERS ---------------- #

def fmt(d):
    return d.strftime("%d %b %Y") if d else ""

# ---------------- FETCH CONTRIBUTIONS ---------------- #

def fetch_contributions():
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

    all_days = []
    total_contributions = 0
    now = datetime.now(timezone.utc)

    for year in range(2008, now.year + 1):
        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = min(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc), now)

        r = requests.post(
            GRAPHQL_URL,
            headers=HEADERS,
            json={"query": query, "variables": {
                "login": GITHUB_USERNAME,
                "from": start.isoformat(),
                "to": end.isoformat()
            }},
            timeout=15
        )

        data = r.json()
        if "errors" in data:
            raise RuntimeError(data["errors"])

        cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        total_contributions += cal["totalContributions"]
        for w in cal["weeks"]:
            all_days.extend(w["contributionDays"])

    return total_contributions, all_days


# ---------------- DAILY COMMITS ---------------- #

_commit_cache = {"ts": None, "data": None}

def fetch_recent_commits():
    global _commit_cache

    # cache 60 seconds
    if _commit_cache["ts"] and (datetime.utcnow() - _commit_cache["ts"]).seconds < 60:
        return _commit_cache["data"]

    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)

    rows = {"today": [], "yesterday": []}

    # get only recently-updated repos
    r = requests.get(
        f"https://api.github.com/user/repos",
        headers=HEADERS,
        params={"per_page": 50, "sort": "pushed"},
        timeout=15
    )

    repos = r.json()

    for repo in repos:
        name = repo["full_name"]

        since = datetime.combine(yesterday, datetime.min.time(), tzinfo=timezone.utc).isoformat()
        until = datetime.combine(today, datetime.max.time(), tzinfo=timezone.utc).isoformat()

        cr = requests.get(
            f"https://api.github.com/repos/{name}/commits",
            headers=HEADERS,
            params={"since": since, "until": until, "per_page": 20},
            timeout=15
        )

        if cr.status_code != 200:
            continue

        for c in cr.json():
            commit = c["commit"]
            ts = datetime.strptime(commit["author"]["date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            d = ts.date()

            rec = {
                "date": d.strftime("%d %b %Y"),
                "time": ts.strftime("%I:%M %p"),
                "msg": commit["message"][:80]
            }

            if d == today:
                rows["today"].append(rec)
            elif d == yesterday:
                rows["yesterday"].append(rec)

    rows["today"].sort(key=lambda x: x["time"], reverse=True)
    rows["yesterday"].sort(key=lambda x: x["time"], reverse=True)

    _commit_cache["ts"] = datetime.utcnow()
    _commit_cache["data"] = rows
    return rows


# ---------------- STATS LOGIC ---------------- #

def calculate_stats(days):
    calendar = {datetime.strptime(d["date"], "%Y-%m-%d").date(): d["contributionCount"] for d in days}
    active_days = [d for d, c in calendar.items() if c > 0]

    total_start, total_end = min(active_days), max(active_days)

    longest = temp = 0
    ls_start = ls_end = None
    cur_start = None

    for d in sorted(calendar):
        if calendar[d] > 0:
            temp += 1
            if temp == 1:
                cur_start = d
            if temp > longest:
                longest, ls_start, ls_end = temp, cur_start, d
        else:
            temp = 0

    today = datetime.now(timezone.utc).date()
    if calendar.get(today, 0) > 0:
        cs_end = today
    elif calendar.get(today - timedelta(days=1), 0) > 0:
        cs_end = today - timedelta(days=1)
    else:
        return {"total_range": (total_start, total_end), "current": 0,
                "current_range": (None, None), "longest": longest,
                "longest_range": (ls_start, ls_end), "calendar": calendar}

    current = 0
    d = cs_end
    cs_start = None

    while calendar.get(d, 0) > 0:
        cs_start = d
        current += 1
        d -= timedelta(days=1)

    return {
        "total_range": (total_start, total_end),
        "current": current,
        "current_range": (cs_start, cs_end),
        "longest": longest,
        "longest_range": (ls_start, ls_end),
        "calendar": calendar
    }


# ---------------- FLASK UI ---------------- #

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>GitHub Streak Dashboard</title>
<style>
body{background:#0d1117;color:white;font-family:Arial;padding:40px;}
.card{display:flex;justify-content:space-around;background:#161b22;padding:30px;border-radius:12px;}
.box{text-align:center;font-size:28px;font-weight:bold;}
.label{font-size:14px;color:#8b949e;}
.sub{font-size:12px;color:#6e7681;}
.heatmap{display:grid;grid-template-columns:repeat(53,12px);gap:3px;margin-top:30px;}
.cell{width:12px;height:12px;border-radius:2px;background:#161b22;}
.l1{background:#0e4429;}
.l2{background:#006d32;}
.l3{background:#26a641;}
.l4{background:#39d353;}
table{width:100%;margin-top:10px;border-collapse:collapse;}
th,td{padding:6px;font-size:12px;text-align:left;}
th{color:#8b949e;}
</style>
</head>
<body>

<h2>🔥 GitHub Streak Dashboard (Exact)</h2>

<div class="card">
<div class="box">{{total}}<div class="label">Total Contributions</div><div class="sub">{{total_start}} → {{total_end}}</div></div>
<div class="box">{{current}}<div class="label">Current Streak</div><div class="sub">{{cs_start}} → {{cs_end}}</div></div>
<div class="box">{{longest}}<div class="label">Longest Streak</div><div class="sub">{{ls_start}} → {{ls_end}}</div></div>
</div>

<div class="heatmap">
{% for c in cells %}<div class="cell {{c}}"></div>{% endfor %}
</div>

<h3 style="margin-top:40px;">🗓 DAILY COMMIT MESSAGE</h3>
<div class="card" style="flex-direction:column;">
<h4>(Yesterday)</h4>
<table><tr><th>Date</th><th>Time</th><th>Commit Message</th></tr>
{% for r in commits.yesterday %}<tr><td>{{r.date}}</td><td>{{r.time}}</td><td>{{r.msg}}</td></tr>{% endfor %}
</table>

<h4>(Today)</h4>
<table><tr><th>Date</th><th>Time</th><th>Commit Message</th></tr>
{% for r in commits.today %}<tr><td>{{r.date}}</td><td>{{r.time}}</td><td>{{r.msg}}</td></tr>{% endfor %}
</table>
</div>

</body></html>
"""

@app.route("/")
def index():
    total, days = fetch_contributions()
    stats = calculate_stats(days)
    commits = fetch_recent_commits()

    today = datetime.now(timezone.utc).date()
    cells = []
    for i in range(365):
        d = today - timedelta(days=364 - i)
        c = stats["calendar"].get(d, 0)
        lvl = "" if c == 0 else "l1" if c < 3 else "l2" if c < 6 else "l3" if c < 10 else "l4"
        cells.append(lvl)

    return render_template_string(
        HTML,
        total=total,
        total_start=fmt(stats["total_range"][0]),
        total_end=fmt(stats["total_range"][1]),
        current=stats["current"],
        cs_start=fmt(stats["current_range"][0]),
        cs_end=fmt(stats["current_range"][1]),
        longest=stats["longest"],
        ls_start=fmt(stats["longest_range"][0]),
        ls_end=fmt(stats["longest_range"][1]),
        cells=cells,
        commits=commits
    )

if __name__ == "__main__":
    app.run(debug=True)















# #!/usr/bin/env python3
# """
# GitHub Streak Dashboard — EXACT (Africa/Lagos timezone aligned)
# """

# import os
# import requests
# import pytz
# from datetime import datetime, timedelta, timezone
# from flask import Flask, render_template_string
# from dotenv import load_dotenv

# load_dotenv()

# # ---------------- CONFIG ---------------- #

# GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
# TOKEN = os.getenv("GITHUB_TOKEN")

# if not GITHUB_USERNAME or not TOKEN:
#     raise RuntimeError("GITHUB_USERNAME or GITHUB_TOKEN missing")

# GRAPHQL_URL = "https://api.github.com/graphql"
# LOCAL_TZ = pytz.timezone("Africa/Lagos")

# HEADERS = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Accept": "application/vnd.github+json"
# }

# # ---------------- HELPERS ---------------- #

# def fmt(d):
#     return d.strftime("%d %b %Y") if d else ""

# # ---------------- FETCH CONTRIBUTIONS ---------------- #

# def fetch_contributions():
#     query = """
#     query($login: String!, $from: DateTime!, $to: DateTime!) {
#       user(login: $login) {
#         contributionsCollection(from: $from, to: $to) {
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

#     all_days = []
#     total_contributions = 0
#     now = datetime.now(timezone.utc)

#     for year in range(2008, now.year + 1):
#         start = datetime(year, 1, 1, tzinfo=timezone.utc)
#         end = min(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc), now)

#         r = requests.post(
#             GRAPHQL_URL,
#             headers=HEADERS,
#             json={"query": query, "variables": {
#                 "login": GITHUB_USERNAME,
#                 "from": start.isoformat(),
#                 "to": end.isoformat()
#             }},
#             timeout=15
#         )

#         data = r.json()
#         if "errors" in data:
#             raise RuntimeError(data["errors"])

#         cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
#         total_contributions += cal["totalContributions"]
#         for w in cal["weeks"]:
#             all_days.extend(w["contributionDays"])

#     return total_contributions, all_days

# # ---------------- DAILY COMMITS ---------------- #

# _commit_cache = {"ts": None, "data": None}

# def fetch_recent_commits():
#     global _commit_cache

#     if _commit_cache["ts"] and (datetime.utcnow() - _commit_cache["ts"]).seconds < 60:
#         return _commit_cache["data"]

#     today = datetime.now(LOCAL_TZ).date()
#     yesterday = today - timedelta(days=1)

#     rows = {"today": [], "yesterday": []}

#     r = requests.get(
#         f"https://api.github.com/user/repos",
#         headers=HEADERS,
#         params={"per_page": 50, "sort": "pushed"},
#         timeout=15
#     )

#     for repo in r.json():
#         name = repo["full_name"]

#         since = datetime.combine(yesterday, datetime.min.time(), tzinfo=LOCAL_TZ).astimezone(timezone.utc).isoformat()
#         until = datetime.combine(today, datetime.max.time(), tzinfo=LOCAL_TZ).astimezone(timezone.utc).isoformat()

#         cr = requests.get(
#             f"https://api.github.com/repos/{name}/commits",
#             headers=HEADERS,
#             params={"since": since, "until": until, "per_page": 20},
#             timeout=15
#         )

#         if cr.status_code != 200:
#             continue

#         for c in cr.json():
#             commit = c["commit"]
#             ts = datetime.strptime(commit["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
#             ts = ts.replace(tzinfo=timezone.utc).astimezone(LOCAL_TZ)
#             d = ts.date()

#             rec = {
#                 "date": d.strftime("%d %b %Y"),
#                 "time": ts.strftime("%I:%M %p"),
#                 "msg": commit["message"][:80]
#             }

#             if d == today:
#                 rows["today"].append(rec)
#             elif d == yesterday:
#                 rows["yesterday"].append(rec)

#     rows["today"].sort(key=lambda x: x["time"], reverse=True)
#     rows["yesterday"].sort(key=lambda x: x["time"], reverse=True)

#     _commit_cache["ts"] = datetime.utcnow()
#     _commit_cache["data"] = rows
#     return rows

# # ---------------- STATS LOGIC ---------------- #

# def calculate_stats(days):
#     calendar = {datetime.strptime(d["date"], "%Y-%m-%d").date(): d["contributionCount"] for d in days}
#     active_days = [d for d, c in calendar.items() if c > 0]

#     total_start, total_end = min(active_days), max(active_days)

#     longest = temp = 0
#     ls_start = ls_end = None
#     cur_start = None

#     for d in sorted(calendar):
#         if calendar[d] > 0:
#             temp += 1
#             if temp == 1:
#                 cur_start = d
#             if temp > longest:
#                 longest, ls_start, ls_end = temp, cur_start, d
#         else:
#             temp = 0

#     today = datetime.now(LOCAL_TZ).date()
#     if calendar.get(today, 0) > 0:
#         cs_end = today
#     elif calendar.get(today - timedelta(days=1), 0) > 0:
#         cs_end = today - timedelta(days=1)
#     else:
#         return {"total_range": (total_start, total_end), "current": 0,
#                 "current_range": (None, None), "longest": longest,
#                 "longest_range": (ls_start, ls_end), "calendar": calendar}

#     current = 0
#     d = cs_end
#     cs_start = None

#     while calendar.get(d, 0) > 0:
#         cs_start = d
#         current += 1
#         d -= timedelta(days=1)

#     return {
#         "total_range": (total_start, total_end),
#         "current": current,
#         "current_range": (cs_start, cs_end),
#         "longest": longest,
#         "longest_range": (ls_start, ls_end),
#         "calendar": calendar
#     }

# # ---------------- FLASK UI ---------------- #

# app = Flask(__name__)

# # (HTML unchanged)

# @app.route("/")
# def index():
#     total, days = fetch_contributions()
#     stats = calculate_stats(days)
#     commits = fetch_recent_commits()

#     today = datetime.now(LOCAL_TZ).date()
#     cells = []
#     for i in range(365):
#         d = today - timedelta(days=364 - i)
#         c = stats["calendar"].get(d, 0)
#         lvl = "" if c == 0 else "l1" if c < 3 else "l2" if c < 6 else "l3" if c < 10 else "l4"
#         cells.append(lvl)

#     return render_template_string(
#         HTML,
#         total=total,
#         total_start=fmt(stats["total_range"][0]),
#         total_end=fmt(stats["total_range"][1]),
#         current=stats["current"],
#         cs_start=fmt(stats["current_range"][0]),
#         cs_end=fmt(stats["current_range"][1]),
#         longest=stats["longest"],
#         ls_start=fmt(stats["longest_range"][0]),
#         ls_end=fmt(stats["longest_range"][1]),
#         cells=cells,
#         commits=commits
#     )

# if __name__ == "__main__":
#     app.run(debug=True)


















# #!/usr/bin/env python3
# """
# GitHub Streak Dashboard — EXACT (Matches GitHub)
# """

# import os
# import requests
# from datetime import datetime, timedelta, date, timezone
# from flask import Flask, render_template_string
# from dotenv import load_dotenv

# load_dotenv()

# # ---------------- CONFIG ---------------- #

# GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
# TOKEN = os.getenv("GITHUB_TOKEN")

# if not GITHUB_USERNAME or not TOKEN:
#     raise RuntimeError("GITHUB_USERNAME or GITHUB_TOKEN missing")

# GRAPHQL_URL = "https://api.github.com/graphql"

# HEADERS = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Accept": "application/vnd.github+json"
# }

# # ---------------- HELPERS ---------------- #

# def fmt(d):
#     return d.strftime("%d %b %Y") if d else ""

# # ---------------- FETCH CONTRIBUTIONS ---------------- #

# def fetch_contributions():
#     query = """
#     query($login: String!, $from: DateTime!, $to: DateTime!) {
#       user(login: $login) {
#         contributionsCollection(from: $from, to: $to) {
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

#     all_days = []
#     total_contributions = 0
#     now = datetime.now(timezone.utc)

#     for year in range(2008, now.year + 1):
#         start = datetime(year, 1, 1, tzinfo=timezone.utc)
#         end = min(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc), now)

#         r = requests.post(
#             GRAPHQL_URL,
#             headers=HEADERS,
#             json={"query": query, "variables": {
#                 "login": GITHUB_USERNAME,
#                 "from": start.isoformat(),
#                 "to": end.isoformat()
#             }},
#             timeout=15
#         )

#         data = r.json()
#         if "errors" in data:
#             raise RuntimeError(data["errors"])

#         cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
#         total_contributions += cal["totalContributions"]
#         for w in cal["weeks"]:
#             all_days.extend(w["contributionDays"])

#     return total_contributions, all_days


# # ---------------- DAILY COMMITS ---------------- #

# _commit_cache = {"ts": None, "data": None}

# def fetch_recent_commits():
#     global _commit_cache

#     # cache 60 seconds
#     if _commit_cache["ts"] and (datetime.utcnow() - _commit_cache["ts"]).seconds < 60:
#         return _commit_cache["data"]

#     today = datetime.now(timezone.utc).date()
#     yesterday = today - timedelta(days=1)

#     rows = {"today": [], "yesterday": []}

#     # get only recently-updated repos
#     r = requests.get(
#         f"https://api.github.com/user/repos",
#         headers=HEADERS,
#         params={"per_page": 50, "sort": "pushed"},
#         timeout=15
#     )

#     repos = r.json()

#     for repo in repos:
#         name = repo["full_name"]

#         since = datetime.combine(yesterday, datetime.min.time(), tzinfo=timezone.utc).isoformat()
#         until = datetime.combine(today, datetime.max.time(), tzinfo=timezone.utc).isoformat()

#         cr = requests.get(
#             f"https://api.github.com/repos/{name}/commits",
#             headers=HEADERS,
#             params={"since": since, "until": until, "per_page": 20},
#             timeout=15
#         )

#         if cr.status_code != 200:
#             continue

#         for c in cr.json():
#             commit = c["commit"]
#             ts = datetime.strptime(commit["author"]["date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
#             d = ts.date()

#             rec = {
#                 "date": d.strftime("%d %b %Y"),
#                 "time": ts.strftime("%I:%M %p"),
#                 "msg": commit["message"][:80]
#             }

#             if d == today:
#                 rows["today"].append(rec)
#             elif d == yesterday:
#                 rows["yesterday"].append(rec)

#     rows["today"].sort(key=lambda x: x["time"], reverse=True)
#     rows["yesterday"].sort(key=lambda x: x["time"], reverse=True)

#     _commit_cache["ts"] = datetime.utcnow()
#     _commit_cache["data"] = rows
#     return rows


# # ---------------- STATS LOGIC ---------------- #

# def calculate_stats(days):
#     calendar = {datetime.strptime(d["date"], "%Y-%m-%d").date(): d["contributionCount"] for d in days}
#     active_days = [d for d, c in calendar.items() if c > 0]

#     total_start, total_end = min(active_days), max(active_days)

#     longest = temp = 0
#     ls_start = ls_end = None
#     cur_start = None

#     for d in sorted(calendar):
#         if calendar[d] > 0:
#             temp += 1
#             if temp == 1:
#                 cur_start = d
#             if temp > longest:
#                 longest, ls_start, ls_end = temp, cur_start, d
#         else:
#             temp = 0

#     today = datetime.now(timezone.utc).date()
#     if calendar.get(today, 0) > 0:
#         cs_end = today
#     elif calendar.get(today - timedelta(days=1), 0) > 0:
#         cs_end = today - timedelta(days=1)
#     else:
#         return {"total_range": (total_start, total_end), "current": 0,
#                 "current_range": (None, None), "longest": longest,
#                 "longest_range": (ls_start, ls_end), "calendar": calendar}

#     current = 0
#     d = cs_end
#     cs_start = None

#     while calendar.get(d, 0) > 0:
#         cs_start = d
#         current += 1
#         d -= timedelta(days=1)

#     return {
#         "total_range": (total_start, total_end),
#         "current": current,
#         "current_range": (cs_start, cs_end),
#         "longest": longest,
#         "longest_range": (ls_start, ls_end),
#         "calendar": calendar
#     }


# # ---------------- FLASK UI ---------------- #

# app = Flask(__name__)

# HTML = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>GitHub Streak Dashboard</title>
# <style>
# body{background:#0d1117;color:white;font-family:Arial;padding:40px;}
# .card{display:flex;justify-content:space-around;background:#161b22;padding:30px;border-radius:12px;}
# .box{text-align:center;font-size:28px;font-weight:bold;}
# .label{font-size:14px;color:#8b949e;}
# .sub{font-size:12px;color:#6e7681;}
# .heatmap{display:grid;grid-template-columns:repeat(53,12px);gap:3px;margin-top:30px;}
# .cell{width:12px;height:12px;border-radius:2px;background:#161b22;}
# .l1{background:#0e4429;}
# .l2{background:#006d32;}
# .l3{background:#26a641;}
# .l4{background:#39d353;}
# table{width:100%;margin-top:10px;border-collapse:collapse;}
# th,td{padding:6px;font-size:12px;text-align:left;}
# th{color:#8b949e;}
# </style>
# </head>
# <body>

# <h2>🔥 GitHub Streak Dashboard (Exact)</h2>

# <div class="card">
# <div class="box">{{total}}<div class="label">Total Contributions</div><div class="sub">{{total_start}} → {{total_end}}</div></div>
# <div class="box">{{current}}<div class="label">Current Streak</div><div class="sub">{{cs_start}} → {{cs_end}}</div></div>
# <div class="box">{{longest}}<div class="label">Longest Streak</div><div class="sub">{{ls_start}} → {{ls_end}}</div></div>
# </div>

# <div class="heatmap">
# {% for c in cells %}<div class="cell {{c}}"></div>{% endfor %}
# </div>

# <h3 style="margin-top:40px;">🗓 DAILY COMMIT MESSAGE</h3>
# <div class="card" style="flex-direction:column;">
# <h4>(Yesterday)</h4>
# <table><tr><th>Date</th><th>Time</th><th>Commit Message</th></tr>
# {% for r in commits.yesterday %}<tr><td>{{r.date}}</td><td>{{r.time}}</td><td>{{r.msg}}</td></tr>{% endfor %}
# </table>

# <h4>(Today)</h4>
# <table><tr><th>Date</th><th>Time</th><th>Commit Message</th></tr>
# {% for r in commits.today %}<tr><td>{{r.date}}</td><td>{{r.time}}</td><td>{{r.msg}}</td></tr>{% endfor %}
# </table>
# </div>

# </body></html>
# """

# @app.route("/")
# def index():
#     total, days = fetch_contributions()
#     stats = calculate_stats(days)
#     commits = fetch_recent_commits()

#     today = datetime.now(timezone.utc).date()
#     cells = []
#     for i in range(365):
#         d = today - timedelta(days=364 - i)
#         c = stats["calendar"].get(d, 0)
#         lvl = "" if c == 0 else "l1" if c < 3 else "l2" if c < 6 else "l3" if c < 10 else "l4"
#         cells.append(lvl)

#     return render_template_string(
#         HTML,
#         total=total,
#         total_start=fmt(stats["total_range"][0]),
#         total_end=fmt(stats["total_range"][1]),
#         current=stats["current"],
#         cs_start=fmt(stats["current_range"][0]),
#         cs_end=fmt(stats["current_range"][1]),
#         longest=stats["longest"],
#         ls_start=fmt(stats["longest_range"][0]),
#         ls_end=fmt(stats["longest_range"][1]),
#         cells=cells,
#         commits=commits
#     )

# if __name__ == "__main__":
#     app.run(debug=True)






























# #!/usr/bin/env python3
# """
# GitHub Streak Dashboard — EXACT (Matches GitHub)
# """

# import os
# import requests
# from datetime import datetime, timedelta, date, timezone
# from flask import Flask, render_template_string
# from dotenv import load_dotenv

# load_dotenv()

# # ---------------- CONFIG ---------------- #

# GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
# TOKEN = os.getenv("GITHUB_TOKEN")

# if not GITHUB_USERNAME or not TOKEN:
#     raise RuntimeError("GITHUB_USERNAME or GITHUB_TOKEN missing")

# GRAPHQL_URL = "https://api.github.com/graphql"

# HEADERS = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Accept": "application/vnd.github+json"
# }

# # ---------------- HELPERS ---------------- #

# def fmt(d):
#     return d.strftime("%d %b %Y") if d else ""

# # ---------------- FETCH DATA (YEAR BY YEAR) ---------------- #

# def fetch_contributions():
#     query = """
#     query($login: String!, $from: DateTime!, $to: DateTime!) {
#       user(login: $login) {
#         contributionsCollection(from: $from, to: $to) {
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

#     all_days = []
#     total_contributions = 0

#     now = datetime.now(timezone.utc)
#     start_year = 2008
#     end_year = now.year

#     for year in range(start_year, end_year + 1):
#         start = datetime(year, 1, 1, tzinfo=timezone.utc)
#         end = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
#         if end > now:
#             end = now

#         r = requests.post(
#             GRAPHQL_URL,
#             headers=HEADERS,
#             json={
#                 "query": query,
#                 "variables": {
#                     "login": GITHUB_USERNAME,
#                     "from": start.isoformat(),
#                     "to": end.isoformat()
#                 }
#             },
#             timeout=15
#         )

#         data = r.json()
#         if "errors" in data:
#             raise RuntimeError(data["errors"])

#         cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
#         total_contributions += cal["totalContributions"]

#         for w in cal["weeks"]:
#             all_days.extend(w["contributionDays"])

#     return total_contributions, all_days


# # ---------------- FETCH Daily Commits (Daily) ---------------- #
# def fetch_recent_commits():
#     url = f"https://api.github.com/users/{GITHUB_USERNAME}/events"
#     r = requests.get(url, headers=HEADERS, timeout=15)
#     data = r.json()

#     today = datetime.now(timezone.utc).date()
#     yesterday = today - timedelta(days=1)

#     rows = {"today": [], "yesterday": []}

#     for ev in data:
#         if ev["type"] == "PushEvent":
#             for c in ev["payload"]["commits"]:
#                 ts = datetime.strptime(ev["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
#                 d = ts.date()
#                 rec = {
#                     "date": d.strftime("%d %b %Y"),
#                     "time": ts.strftime("%I:%M %p"),
#                     "msg": c["message"][:80]
#                 }

#                 if d == today:
#                     rows["today"].append(rec)
#                 elif d == yesterday:
#                     rows["yesterday"].append(rec)

#     return rows



# # ---------------- STATS LOGIC ---------------- #

# def calculate_stats(days):
#     calendar = {
#         datetime.strptime(d["date"], "%Y-%m-%d").date(): d["contributionCount"]
#         for d in days
#     }

#     active_days = [d for d, c in calendar.items() if c > 0]

#     total_start = min(active_days)
#     total_end = max(active_days)

#     # ---------- LONGEST STREAK ----------
#     longest = 0
#     temp = 0
#     ls_start = ls_end = None
#     cur_start = None

#     for d in sorted(calendar):
#         if calendar[d] > 0:
#             temp += 1
#             if temp == 1:
#                 cur_start = d
#             if temp > longest:
#                 longest = temp
#                 ls_start = cur_start
#                 ls_end = d
#         else:
#             temp = 0

#     # ---------- CURRENT STREAK (GitHub UTC EXACT) ----------
#     today = datetime.now(timezone.utc).date()

#     if calendar.get(today, 0) > 0:
#         cs_end = today
#     elif calendar.get(today - timedelta(days=1), 0) > 0:
#         cs_end = today - timedelta(days=1)
#     else:
#         return {
#             "total_range": (total_start, total_end),
#             "current": 0,
#             "current_range": (None, None),
#             "longest": longest,
#             "longest_range": (ls_start, ls_end),
#             "calendar": calendar
#         }

#     current = 0
#     cs_start = None
#     d = cs_end

#     while calendar.get(d, 0) > 0:
#         cs_start = d
#         current += 1
#         d -= timedelta(days=1)

#     return {
#         "total_range": (total_start, total_end),
#         "current": current,
#         "current_range": (cs_start, cs_end),
#         "longest": longest,
#         "longest_range": (ls_start, ls_end),
#         "calendar": calendar
#     }

# # ---------------- FLASK UI ---------------- #

# app = Flask(__name__)

# HTML = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>GitHub Streak Dashboard</title>
# <style>
# body{background:#0d1117;color:white;font-family:Arial;padding:40px;}
# .card{display:flex;justify-content:space-around;background:#161b22;padding:30px;border-radius:12px;}
# .box{text-align:center;font-size:28px;font-weight:bold;}
# .label{font-size:14px;color:#8b949e;}
# .sub{font-size:12px;color:#6e7681;}
# .heatmap{display:grid;grid-template-columns:repeat(53,12px);gap:3px;margin-top:30px;}
# .cell{width:12px;height:12px;border-radius:2px;background:#161b22;}
# .l1{background:#0e4429;}
# .l2{background:#006d32;}
# .l3{background:#26a641;}
# .l4{background:#39d353;}
# </style>
# </head>
# <body>

# <h2>🔥 GitHub Streak Dashboard (Exact)</h2>

# <div class="card">

# <div class="box">
# {{total}}
# <div class="label">Total Contributions</div>
# <div class="sub">{{total_start}} → {{total_end}}</div>
# </div>

# <div class="box">
# {{current}}
# <div class="label">Current Streak</div>
# {% if cs_start %}
# <div class="sub">{{cs_start}} → {{cs_end}}</div>
# {% endif %}
# </div>

# <div class="box">
# {{longest}}
# <div class="label">Longest Streak</div>
# <div class="sub">{{ls_start}} → {{ls_end}}</div>
# </div>

# </div>

# <div class="heatmap">
# {% for c in cells %}
# <div class="cell {{c}}"></div>
# {% endfor %}
# </div>

# </body>
# </html>
# """

# @app.route("/")
# def index():
#     total, days = fetch_contributions()
#     stats = calculate_stats(days)

#     today = datetime.now(timezone.utc).date()
#     cells = []

#     for i in range(365):
#         d = today - timedelta(days=364 - i)
#         c = stats["calendar"].get(d, 0)
#         if c == 0: lvl=""
#         elif c < 3: lvl="l1"
#         elif c < 6: lvl="l2"
#         elif c < 10: lvl="l3"
#         else: lvl="l4"
#         cells.append(lvl)

#     return render_template_string(
#         HTML,
#         total=total,
#         total_start=fmt(stats["total_range"][0]),
#         total_end=fmt(stats["total_range"][1]),
#         current=stats["current"],
#         cs_start=fmt(stats["current_range"][0]),
#         cs_end=fmt(stats["current_range"][1]),
#         longest=stats["longest"],
#         ls_start=fmt(stats["longest_range"][0]),
#         ls_end=fmt(stats["longest_range"][1]),
#         cells=cells
#     )

# if __name__ == "__main__":
#     app.run(debug=True)

















# #!/usr/bin/env python3
# """
# GitHub Streak Dashboard — EXACT (Matches GitHub)
# """

# import os
# import requests
# from datetime import datetime, timedelta, date, timezone
# from flask import Flask, render_template_string
# from dotenv import load_dotenv

# load_dotenv()

# # ---------------- CONFIG ---------------- #

# GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
# TOKEN = os.getenv("GITHUB_TOKEN")

# if not GITHUB_USERNAME or not TOKEN:
#     raise RuntimeError("GITHUB_USERNAME or GITHUB_TOKEN missing")

# GRAPHQL_URL = "https://api.github.com/graphql"

# HEADERS = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Accept": "application/vnd.github+json"
# }

# # ---------------- HELPERS ---------------- #

# def fmt(d):
#     return d.strftime("%d %b %Y") if d else ""

# # ---------------- FETCH DATA (YEAR BY YEAR) ---------------- #

# def fetch_contributions():
#     query = """
#     query($login: String!, $from: DateTime!, $to: DateTime!) {
#       user(login: $login) {
#         contributionsCollection(from: $from, to: $to) {
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

#     all_days = []
#     total_contributions = 0

#     now = datetime.now(timezone.utc)
#     start_year = 2008
#     end_year = now.year

#     for year in range(start_year, end_year + 1):
#         start = datetime(year, 1, 1, tzinfo=timezone.utc)
#         end = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
#         if end > now:
#             end = now

#         r = requests.post(
#             GRAPHQL_URL,
#             headers=HEADERS,
#             json={
#                 "query": query,
#                 "variables": {
#                     "login": GITHUB_USERNAME,
#                     "from": start.isoformat(),
#                     "to": end.isoformat()
#                 }
#             },
#             timeout=15
#         )

#         data = r.json()
#         if "errors" in data:
#             raise RuntimeError(data["errors"])

#         cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
#         total_contributions += cal["totalContributions"]

#         for w in cal["weeks"]:
#             all_days.extend(w["contributionDays"])

#     return total_contributions, all_days

# # ---------------- STATS LOGIC ---------------- #

# def calculate_stats(days):
#     calendar = {
#         datetime.strptime(d["date"], "%Y-%m-%d").date(): d["contributionCount"]
#         for d in days
#     }

#     active_days = [d for d, c in calendar.items() if c > 0]

#     total_start = min(active_days)
#     total_end = max(active_days)

#     # ---------- LONGEST STREAK ----------
#     longest = 0
#     temp = 0
#     ls_start = ls_end = None
#     cur_start = None

#     for d in sorted(calendar):
#         if calendar[d] > 0:
#             temp += 1
#             if temp == 1:
#                 cur_start = d
#             if temp > longest:
#                 longest = temp
#                 ls_start = cur_start
#                 ls_end = d
#         else:
#             temp = 0

#     # ---------- CURRENT STREAK (FIXED — GitHub exact) ----------
#     today = date.today()

#     if calendar.get(today, 0) > 0:
#         cs_end = today
#     elif calendar.get(today - timedelta(days=1), 0) > 0:
#         cs_end = today - timedelta(days=1)
#     else:
#         return {
#             "total_range": (total_start, total_end),
#             "current": 0,
#             "current_range": (None, None),
#             "longest": longest,
#             "longest_range": (ls_start, ls_end),
#             "calendar": calendar
#         }

#     current = 0
#     cs_start = None
#     d = cs_end

#     while calendar.get(d, 0) > 0:
#         cs_start = d
#         current += 1
#         d -= timedelta(days=1)

#     return {
#         "total_range": (total_start, total_end),
#         "current": current,
#         "current_range": (cs_start, cs_end),
#         "longest": longest,
#         "longest_range": (ls_start, ls_end),
#         "calendar": calendar
#     }

# # ---------------- FLASK UI ---------------- #

# app = Flask(__name__)

# HTML = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>GitHub Streak Dashboard</title>
# <style>
# body{background:#0d1117;color:white;font-family:Arial;padding:40px;}
# .card{display:flex;justify-content:space-around;background:#161b22;padding:30px;border-radius:12px;}
# .box{text-align:center;font-size:28px;font-weight:bold;}
# .label{font-size:14px;color:#8b949e;}
# .sub{font-size:12px;color:#6e7681;}
# .heatmap{display:grid;grid-template-columns:repeat(53,12px);gap:3px;margin-top:30px;}
# .cell{width:12px;height:12px;border-radius:2px;background:#161b22;}
# .l1{background:#0e4429;}
# .l2{background:#006d32;}
# .l3{background:#26a641;}
# .l4{background:#39d353;}
# </style>
# </head>
# <body>

# <h2>🔥 GitHub Streak Dashboard (Exact)</h2>

# <div class="card">

# <div class="box">
# {{total}}
# <div class="label">Total Contributions</div>
# <div class="sub">{{total_start}} → {{total_end}}</div>
# </div>

# <div class="box">
# {{current}}
# <div class="label">Current Streak</div>
# {% if cs_start %}
# <div class="sub">{{cs_start}} → {{cs_end}}</div>
# {% endif %}
# </div>

# <div class="box">
# {{longest}}
# <div class="label">Longest Streak</div>
# <div class="sub">{{ls_start}} → {{ls_end}}</div>
# </div>

# </div>

# <div class="heatmap">
# {% for c in cells %}
# <div class="cell {{c}}"></div>
# {% endfor %}
# </div>

# </body>
# </html>
# """

# @app.route("/")
# def index():
#     total, days = fetch_contributions()
#     stats = calculate_stats(days)

#     today = date.today()
#     cells = []

#     for i in range(365):
#         d = today - timedelta(days=364 - i)
#         c = stats["calendar"].get(d, 0)
#         if c == 0: lvl=""
#         elif c < 3: lvl="l1"
#         elif c < 6: lvl="l2"
#         elif c < 10: lvl="l3"
#         else: lvl="l4"
#         cells.append(lvl)

#     return render_template_string(
#         HTML,
#         total=total,
#         total_start=fmt(stats["total_range"][0]),
#         total_end=fmt(stats["total_range"][1]),
#         current=stats["current"],
#         cs_start=fmt(stats["current_range"][0]),
#         cs_end=fmt(stats["current_range"][1]),
#         longest=stats["longest"],
#         ls_start=fmt(stats["longest_range"][0]),
#         ls_end=fmt(stats["longest_range"][1]),
#         cells=cells
#     )

# if __name__ == "__main__":
#     app.run(debug=True)















# #!/usr/bin/env python3
# """
# GitHub Streak Dashboard — EXACT (Matches GitHub)
# """

# import os
# import requests
# from datetime import datetime, timedelta, date, timezone
# from flask import Flask, render_template_string
# from dotenv import load_dotenv

# load_dotenv()

# # ---------------- CONFIG ---------------- #

# GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
# TOKEN = os.getenv("GITHUB_TOKEN")

# GRAPHQL_URL = "https://api.github.com/graphql"

# HEADERS = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Accept": "application/vnd.github+json"
# }

# # ---------------- HELPERS ---------------- #

# def fmt(d):
#     return d.strftime("%d %b %Y")

# # ---------------- FETCH DATA ---------------- #

# def fetch_contributions():
#     start = datetime(2008, 1, 1, tzinfo=timezone.utc)  # GitHub founding year
#     end = datetime.now(timezone.utc)

#     query = """
#     query($login: String!, $from: DateTime!, $to: DateTime!) {
#       user(login: $login) {
#         contributionsCollection(from: $from, to: $to) {
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
#         json={
#             "query": query,
#             "variables": {
#                 "login": GITHUB_USERNAME,
#                 "from": start.isoformat(),
#                 "to": end.isoformat()
#             }
#         },
#         headers=HEADERS,
#         timeout=15
#     )

#     data = r.json()
#     if "errors" in data:
#         raise RuntimeError(data["errors"])

#     return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]

# # ---------------- STREAK LOGIC ---------------- #

# def calculate_stats(days):
#     calendar = {
#         datetime.strptime(d["date"], "%Y-%m-%d").date(): d["contributionCount"]
#         for d in days
#     }

#     all_dates = [d for d, c in calendar.items() if c > 0]
#     total_start = min(all_dates)
#     total_end = max(all_dates)

#     # ---------- LONGEST STREAK ----------
#     longest = 0
#     temp = 0
#     ls_start = ls_end = None
#     cur_start = None

#     for d in sorted(calendar):
#         if calendar[d] > 0:
#             temp += 1
#             if temp == 1:
#                 cur_start = d
#             if temp > longest:
#                 longest = temp
#                 ls_start = cur_start
#                 ls_end = d
#         else:
#             temp = 0

#     # ---------- CURRENT STREAK ----------
#     today = datetime.now(timezone.utc).date()
#     if calendar.get(today, 0) == 0:
#         today -= timedelta(days=1)

#     cs_end = today
#     cs_start = None
#     current = 0

#     while calendar.get(today, 0) > 0:
#         cs_start = today
#         current += 1
#         today -= timedelta(days=1)

#     return {
#         "total": len(all_dates),
#         "total_range": (total_start, total_end),
#         "current": current,
#         "current_range": (cs_start, cs_end),
#         "longest": longest,
#         "longest_range": (ls_start, ls_end),
#         "calendar": calendar
#     }

# # ---------------- FLASK UI ---------------- #

# app = Flask(__name__)

# HTML = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>GitHub Streak Dashboard</title>
# <style>
# body{background:#0d1117;color:white;font-family:Arial;padding:40px;}
# .card{display:flex;justify-content:space-around;background:#161b22;padding:30px;border-radius:12px;}
# .box{text-align:center;font-size:28px;font-weight:bold;}
# .label{font-size:14px;color:#8b949e;}
# .sub{font-size:12px;color:#6e7681;}
# .heatmap{display:grid;grid-template-columns:repeat(53,12px);gap:3px;margin-top:30px;}
# .cell{width:12px;height:12px;border-radius:2px;background:#161b22;}
# .l1{background:#0e4429;}
# .l2{background:#006d32;}
# .l3{background:#26a641;}
# .l4{background:#39d353;}
# </style>
# </head>
# <body>

# <h2>🔥 GitHub Streak Dashboard (Exact)</h2>

# <div class="card">

# <div class="box">
# {{total}}
# <div class="label">Total Contributions</div>
# <div class="sub">{{total_start}} → {{total_end}}</div>
# </div>

# <div class="box">
# {{current}}
# <div class="label">Current Streak</div>
# {% if cs_start %}
# <div class="sub">{{cs_start}} → {{cs_end}}</div>
# {% endif %}
# </div>

# <div class="box">
# {{longest}}
# <div class="label">Longest Streak</div>
# <div class="sub">{{ls_start}} → {{ls_end}}</div>
# </div>

# </div>

# <div class="heatmap">
# {% for c in cells %}
# <div class="cell {{c}}"></div>
# {% endfor %}
# </div>

# </body>
# </html>
# """

# @app.route("/")
# def index():
#     data = fetch_contributions()

#     days = []
#     for w in data["weeks"]:
#         days.extend(w["contributionDays"])

#     stats = calculate_stats(days)

#     today = datetime.now(timezone.utc).date()
#     cells = []

#     for i in range(365):
#         d = today - timedelta(days=364 - i)
#         c = stats["calendar"].get(d, 0)
#         if c == 0: lvl = ""
#         elif c < 3: lvl = "l1"
#         elif c < 6: lvl = "l2"
#         elif c < 10: lvl = "l3"
#         else: lvl = "l4"
#         cells.append(lvl)

#     return render_template_string(
#         HTML,
#         total=data["totalContributions"],
#         total_start=fmt(stats["total_range"][0]),
#         total_end=fmt(stats["total_range"][1]),
#         current=stats["current"],
#         cs_start=fmt(stats["current_range"][0]) if stats["current_range"][0] else None,
#         cs_end=fmt(stats["current_range"][1]) if stats["current_range"][1] else None,
#         longest=stats["longest"],
#         ls_start=fmt(stats["longest_range"][0]),
#         ls_end=fmt(stats["longest_range"][1]),
#         cells=cells
#     )

# if __name__ == "__main__":
#     app.run(debug=True)



























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































