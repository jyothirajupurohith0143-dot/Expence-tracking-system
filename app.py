import streamlit as st
from src.database import init_db
from src.auth import register_user, authenticate_user
from src.dashboard import render_dashboard
from src.transactions import render_transactions
from src.budget import render_budget
from src.reports import render_reports

st.set_page_config(
    page_title="Expense Tracking & Analytics",
    page_icon="💰",
    layout="wide",
)

init_db()

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def login_page():
    st.title("💰 Expense Tracking & Analytics")
    st.caption("Personal finance management and data analytics dashboard")

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            user_id = authenticate_user(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        with st.form("register_form"):
            username = st.text_input("New username")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Register", use_container_width=True)

        if submitted:
            if not username.strip() or not password:
                st.warning("Username and password are required.")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.warning("Password must contain at least 6 characters.")
            elif register_user(username.strip(), password):
                st.success("Account created. Please log in.")
            else:
                st.error("Username already exists.")

if st.session_state.user_id is None:
    login_page()
else:
    with st.sidebar:
        st.title("💰 Finance Tracker")
        st.write(f"Welcome, **{st.session_state.username}**")
        st.divider()

        pages = {
            "📊 Dashboard": "Dashboard",
            "💳 Transactions": "Transactions",
            "🎯 Budget": "Budget",
            "📄 Reports": "Reports",
        }
        selected = st.radio("Navigation", list(pages.keys()))
        st.session_state.page = pages[selected]

        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()

    if st.session_state.page == "Dashboard":
        render_dashboard(st.session_state.user_id)
    elif st.session_state.page == "Transactions":
        render_transactions(st.session_state.user_id)
    elif st.session_state.page == "Budget":
        render_budget(st.session_state.user_id)
    elif st.session_state.page == "Reports":
        render_reports(st.session_state.user_id)
