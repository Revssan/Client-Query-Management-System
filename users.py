import pyodbc
import bcrypt

connection = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=REVS;'
    'DATABASE=Client Query Management System;'
    'Trusted_Connection=yes;'
)

cursor = connection.cursor()

username = "Guna@125.com"
password = "125"
role = "Client"

hashed_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

query = """
INSERT INTO users (username, hashed_password, role)
VALUES (?, ?, ?)
"""

cursor.execute(query, (username, hashed_pwd, role))
connection.commit()

print("User created successfully!")
