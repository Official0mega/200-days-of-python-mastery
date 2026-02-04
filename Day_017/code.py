"""
Day 017 Practice
Author: James
"""

# Write your Python code here
# Day 17 – Web Development (Flask)

from flask import Flask, render_template, request

app = Flask(__name__)

# Route - Home
@app.route("/")
def home():
    return "Hello, world!"

# Route - About
@app.route("/about")
def about():
    return "This is the about page"

# Route - Template example
@app.route("/welcome")
def welcome():
    return render_template("index.html", name="James")

# GET request example
@app.route("/hello")
def hello():
    name = request.args.get("name")
    return f"Hello {name}"

# POST request example
@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    return f"Welcome {username}"

if __name__ == "__main__":
    app.run(debug=True)


# Day 17 – FastAPI Example

from fastapi import FastAPI

api = FastAPI()

@api.get("/home")
def api_home():
    return {"message": "Hello World"}
