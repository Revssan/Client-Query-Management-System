📩 Client Query Management System (CQMS)

A complete Streamlit + SQL Server based application that allows clients to raise queries and support teams to manage and resolve them efficiently.

This system includes:

🔐 Secure Login (with bcrypt password hashing)

👤 Role-based Dashboard (Client / Support)

📊 Track My Queries (Client)

🛠️ Query Management & Status Update (Support)

🗄 SQL Server backend

🐼 Pandas integration for data handling

🚫 Hidden sidebar

🚀 Features

**1️⃣ Login System**

Username + Password + Role selection

Passwords stored using bcrypt hash

Redirects user based on role:

Client → Client Dashboard

Support → Support Dashboard

**2️⃣ Client Dashboard**

**✔ Raise New Query**

Auto-generates unique query_id

**Captures:**

Email

Mobile Number

Query Heading

Description

Timestamp

**✔ Track My Queries**

Shows only the queries raised by logged-in client

**3️⃣ Support Dashboard**

**✔ View Open Queries**

Displays all pending tickets

Filters supported by status

**✔ Update Query**

Change query status:

Open

In Progress

Closed

When closing a query, system auto-adds query_closed_time

