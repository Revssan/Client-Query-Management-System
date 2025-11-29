import streamlit as st
import pyodbc
import bcrypt

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

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

st.markdown("<h1 style='text-align:center;'>🔐 Login Page</h1>",
            unsafe_allow_html=True)


# -------------------------------------------------
# SQL CONNECTION
# -------------------------------------------------
def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=REVS;'
        'DATABASE=Client Query Management System;'
        'Trusted_Connection=yes;'
    )


# -------------------------------------------------
# FETCH ROLES
# -------------------------------------------------
def get_roles():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT role FROM dbo.Users")
    roles = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return roles


# -------------------------------------------------
# LOGIN FUNCTION (bcrypt)
# -------------------------------------------------
def check_login(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT hashed_password, role 
        FROM dbo.Users 
        WHERE username=? AND role=?
    """, (username, role))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        stored_hash = row[0]

        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return username, role

    return None


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None


# -------------------------------------------------
# AUTO REDIRECT BASED ON ROLE
# -------------------------------------------------
if st.session_state.logged_in:

    if st.session_state.role == "Client":
        st.success("Redirecting to Client Dashboard...")
        st.switch_page("pages/Client.py")   # File: pages/1_Client.py

    elif st.session_state.role == "Support":
        st.success("Redirecting to Support Dashboard...")
        st.switch_page("pages/Support.py")  # File: pages/2_Support.py


# -------------------------------------------------
# LOGIN UI
# -------------------------------------------------
if not st.session_state.logged_in:

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        roles = get_roles()

        role = st.selectbox(
            "Select Role",
            roles,
            index=None,
            placeholder="Select Role"
        )

        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            login_btn = st.form_submit_button("Login")

    if login_btn:
        user_data = check_login(username, password, role)

        if user_data:
            st.session_state.logged_in = True
            st.session_state.username = user_data[0]
            st.session_state.role = user_data[1]

            st.success("Login Successful!")
            st.rerun()

        else:
            st.error("Invalid Username, Password, or Role")


# -------------------------------------------------
# LOGOUT (Only visible if logged in, but before redirect)
# -------------------------------------------------
else:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()
