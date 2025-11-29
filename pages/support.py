import streamlit as st
import pyodbc
import pandas as pd

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

st.set_page_config(page_title="Support Dashboard",
                   page_icon="🛠️", layout="centered")


def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=REVS;'
        'DATABASE=Client Query Management System;'
        'Trusted_Connection=yes;'
    )


# ⛔ Prevent access if not logged in
if "logged_in" not in st.session_state or st.session_state.role != "Support":
    st.error("You are not authorized. Please login first.")
    st.switch_page("login.py")

st.markdown("<h1 style='text-align:center;'>🛠️ Support Dashboard</h1>",
            unsafe_allow_html=True)

menu = st.selectbox("Menu", ["View Open Queries", "Update Query"])

# --------------- VIEW OPEN QUERIES ----------------
if menu == "View Open Queries":
    st.header("📂 Open Client Queries")

    conn = get_connection()
    query = """
        SELECT query_id, mail_id, mobile_number, query_heading, query_description,
        status, query_created_time
        FROM [dbo].[ClientManagement]
        WHERE status = 'Open'
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        st.info("No open queries found.")
    else:
        st.dataframe(df, use_container_width=True)


# --------------- UPDATE QUERY ----------------
elif menu == "Update Query":
    with st.form("Query Status"):

        query_id = st.text_input("Enter Query ID to update")
        new_status = st.selectbox(
            "Update Status", ["Open", "In Progress", "Closed"])

        submit_btn = st.form_submit_button("Update")

        if submit_btn:
            conn = get_connection()
            cursor = conn.cursor()

            if new_status == "Closed":
                sql = """
            UPDATE [dbo].[ClientManagement]
            SET status = ?, query_closed_time = GETDATE()
            WHERE query_id = ?
            """
                cursor.execute(sql, (new_status, query_id))
            else:
                sql = "UPDATE [dbo].[ClientManagement] SET status = ? WHERE query_id = ?"
                cursor.execute(sql, (new_status, query_id))

            conn.commit()
            conn.close()

            st.success(f"✅ Query {query_id} updated to **{new_status}**")


if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.switch_page("login.py")
