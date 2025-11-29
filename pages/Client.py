import streamlit as st
import pyodbc
import pandas as pd
from datetime import datetime

# -------------------------------------------------
# HIDE SIDEBAR
# -------------------------------------------------
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="stHeaderActionMenu"] { visibility: hidden !important; }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.set_page_config(page_title="Client Portal",
                   page_icon="📩", layout="centered")

# SQL Server Connection


def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=REVS;'
        'DATABASE=Client Query Management System;'
        'Trusted_Connection=yes;'
    )


# ⛔ Prevent access if not logged in
if "logged_in" not in st.session_state or st.session_state.role != "Client":
    st.error("You are not authorized. Please login first.")
    st.switch_page("login.py")

# Get logged-in user email
# username must be mail_id for clients
logged_email = st.session_state.username

st.markdown("<h1 style='text-align:center;'>📩 Client Query Portal</h1>",
            unsafe_allow_html=True)


menu = st.selectbox("Menu", ["Create Query", "Track My Queries"])

# ---------------- CREATE QUERY ----------------
if menu == "Create Query":
    st.header("📝 Create New Query")

    # ---- FORM START ----
    with st.form("create_query_form"):
        mobile = st.text_input("Mobile Number")
        heading = st.text_input("Query Heading")
        description = st.text_area("Query Description")

        # Submit button inside form
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submit_btn = st.form_submit_button("Submit Query")

    if submit_btn:
        conn = get_connection()
        cursor = conn.cursor()

        query_id = "QRY" + datetime.now().strftime("%Y%m%d%H%M%S")

        insert_sql = """
        INSERT INTO ClientManagement (query_id, mail_id, mobile_number, query_heading,
        query_description, status, query_created_time, query_closed_time)
        VALUES (?, ?, ?, ?, ?, 'Open', GETDATE(), NULL)
        """

        cursor.execute(insert_sql, (query_id, logged_email,
                       mobile, heading, description))
        conn.commit()
        conn.close()

        st.success(
            f"✅ Query Created Successfully! Your Query ID: **{query_id}**")


# ---------------- TRACK MY QUERIES ----------------
elif menu == "Track My Queries":
    st.header("📊 My Queries")

    conn = get_connection()
    query = """
        SELECT query_id, query_heading, status, query_created_time, query_closed_time
        FROM ClientManagement
        WHERE mail_id = ?
        ORDER BY query_created_time DESC
    """

    df = pd.read_sql(query, conn, params=[logged_email])
    conn.close()

    if df.empty:
        st.warning("You have not created any queries yet.")
    else:
        st.dataframe(df, use_container_width=True)

    # --- LOGOUT BUTTON ONLY HERE ---
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.switch_page("login.py")
