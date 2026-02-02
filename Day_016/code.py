"""
Day 016 Practice
Author: James
"""

# Write your Python code here
# Day 16 – Databases

import sqlite3

# Connect to database
connection = sqlite3.connect("users.db")
cursor = connection.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
""")
connection.commit()

# CREATE
cursor.execute("""
INSERT INTO users (name, age)
VALUES (?, ?)
""", ("James", 25))
connection.commit()

# READ
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row)

# UPDATE
cursor.execute("""
UPDATE users
SET age = ?
WHERE name = ?
""", (26, "James"))
connection.commit()

# DELETE
cursor.execute("""
DELETE FROM users
WHERE name = ?
""", ("James",))
connection.commit()

# Close connection
connection.close()


# ORM USING SQLALCHEMY

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

engine = create_engine("sqlite:///users.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# CREATE
new_user = User(name="James", age=25)
session.add(new_user)
session.commit()

# READ
users = session.query(User).all()
for user in users:
    print(user.name, user.age)

# UPDATE
user = session.query(User).filter_by(name="James").first()
user.age = 26
session.commit()

# DELETE
user = session.query(User).filter_by(name="James").first()
session.delete(user)
session.commit()
