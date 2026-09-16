from datetime import date
from io import BytesIO
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Allows the file to work when launched with:
# streamlit run src/dashboard.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.auth import login_user, register_user
from src.database import init_db
from src.transactions import (
    EXPENSE_CATEGORIES,
    INCOME_CATEGORIES,
    add_transaction,
    delete_transaction,
    get_budget,
    get_transactions,
    set_budget,
    update_transaction,
)
from src.analytics import (
    budget_status,
    category_summary,
    monthly_summary,
    summary_metrics,
)


st.set_page_config(
    page_title="Expense Tracking System",
    page_icon="💰",
    layout="wide",
)

init_db()

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Login"


def create_pdf(username, dataframe, month, budget):
    metrics = summary_metrics(dataframe)
    categories = category_summary(dataframe)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, height - 50, "Monthly Expense Report")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, height - 75, f"User: {username}")
    pdf.drawString(50, height - 92, f"Month: {month}")

    y = height - 130
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Summary")
    y -= 20

    pdf.setFont("Helvetica", 10)
    for label, value in [
        ("Income", metrics["income"]),
        ("Expenses", metrics["expense"]),
        ("Savings", metrics["savings"]),
        ("Budget", budget),
    ]:
        pdf.drawString(60, y, f"{label}: Rs. {value:,.2f}")
        y -= 17

    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Expense by Category")
    y -= 20

    pdf.setFont("Helvetica", 10)
    for _, row in categories.iterrows():
        pdf.drawString(
            60,
            y,
            f"{row['category']}: Rs. {row['amount']:,.2f}",
        )
        y -= 17

        if y < 60:
            pdf.showPage()
            y = height - 50

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


def login_page():
    st.title("💰 Expense Tracking System")
    st.write("Track income, expenses, budgets, and savings in one place.")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            user = login_user(username, password)

            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with register_tab:
        with st.form("register_form"):
            new_username = st.text_input("New username")
            new_password = st.text_input("New password", type="password")
            confirm_password = st.text_input(
                "Confirm password",
                type="password",
            )
            submitted = st.form_submit_button("Create account")

        if submitted:
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = register_user(new_username, new_password)

                if success:
                    st.success(message)
                else:
                    st.error(message)


def dashboard_page():
    user = st.session_state.user
    user_id = user["id"]

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Transactions", "Budget & Reports"],
    )

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.title(f"Welcome, {user['username']} 👋")

    if page == "Dashboard":
        show_dashboard(user_id)

    elif page == "Transactions":
        show_transactions(user_id)

    else:
        show_budget_reports(user_id, user["username"])


def show_dashboard(user_id):
    today = date.today()
    month_start = today.replace(day=1).isoformat()
    month_end = today.isoformat()
    month_key = today.strftime("%Y-%m")

    data = get_transactions(user_id, month_start, month_end)
    metrics = summary_metrics(data)
    budget = get_budget(user_id, month_key)
    status, percentage = budget_status(data, budget)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Income", f"Rs. {metrics['income']:,.2f}")
    col2.metric("Expenses", f"Rs. {metrics['expense']:,.2f}")
    col3.metric("Savings", f"Rs. {metrics['savings']:,.2f}")
    col4.metric("Budget", f"Rs. {budget:,.2f}")

    if budget > 0:
        st.progress(min(percentage / 100, 1.0))
        st.info(f"{status} — {percentage:.1f}% of monthly budget used.")
    else:
        st.info("Set a monthly budget from Budget & Reports.")

    st.subheader("Expense by Category")
    categories = category_summary(data)

    if categories.empty:
        st.info("No expenses recorded for this month.")
    else:
        chart = px.pie(
            categories,
            names="category",
            values="amount",
            hole=0.4,
            title="Monthly Expense Distribution",
        )
        st.plotly_chart(chart, use_container_width=True)

    st.subheader("Recent Transactions")
    st.dataframe(data.head(10), use_container_width=True, hide_index=True)


def show_transactions(user_id):
    st.header("Transactions")

    with st.form("transaction_form", clear_on_submit=True):
        transaction_type = st.selectbox(
            "Type",
            ["Expense", "Income"],
        )

        category_options = (
            EXPENSE_CATEGORIES
            if transaction_type == "Expense"
            else INCOME_CATEGORIES
        )

        col1, col2 = st.columns(2)

        with col1:
            amount = st.number_input(
                "Amount",
                min_value=0.01,
                step=100.0,
            )
            category = st.selectbox("Category", category_options)

        with col2:
            transaction_date = st.date_input(
                "Date",
                value=date.today(),
            )
            description = st.text_input("Description")

        submitted = st.form_submit_button("Add Transaction")

    if submitted:
        add_transaction(
            user_id,
            transaction_type,
            amount,
            category,
            description,
            transaction_date.isoformat(),
        )
        st.success("Transaction added successfully.")
        st.rerun()

    st.divider()
    st.subheader("All Transactions")

    data = get_transactions(user_id)

    if data.empty:
        st.info("No transactions found.")
        return

    st.dataframe(data, use_container_width=True, hide_index=True)

    csv_data = data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Transactions CSV",
        data=csv_data,
        file_name="transactions.csv",
        mime="text/csv",
    )

    st.subheader("Manage a Transaction")

    selected_id = st.selectbox(
        "Select transaction ID",
        data["id"].tolist(),
    )

    selected = data[data["id"] == selected_id].iloc[0]

    with st.form("edit_transaction_form"):
        edit_type = st.selectbox(
            "Type",
            ["Expense", "Income"],
            index=0 if selected["transaction_type"] == "Expense" else 1,
        )

        edit_categories = (
            EXPENSE_CATEGORIES
            if edit_type == "Expense"
            else INCOME_CATEGORIES
        )

        current_category = (
            selected["category"]
            if selected["category"] in edit_categories
            else edit_categories[0]
        )

        edit_category = st.selectbox(
            "Category",
            edit_categories,
            index=edit_categories.index(current_category),
        )

        edit_amount = st.number_input(
            "Amount",
            min_value=0.01,
            value=float(selected["amount"]),
            step=100.0,
        )

        edit_description = st.text_input(
            "Description",
            value=str(selected["description"] or ""),
        )

        edit_date = st.date_input(
            "Date",
            value=pd.to_datetime(selected["transaction_date"]).date(),
        )

        update_clicked = st.form_submit_button("Update Transaction")

    if update_clicked:
        update_transaction(
            selected_id,
            user_id,
            edit_type,
            edit_amount,
            edit_category,
            edit_description,
            edit_date.isoformat(),
        )
        st.success("Transaction updated.")
        st.rerun()

    if st.button("Delete Selected Transaction"):
        delete_transaction(selected_id, user_id)
        st.success("Transaction deleted.")
        st.rerun()


def show_budget_reports(user_id, username):
    st.header("Budget & Reports")

    today = date.today()
    month_key = today.strftime("%Y-%m")

    st.subheader("Set Monthly Budget")

    current_budget = get_budget(user_id, month_key)

    with st.form("budget_form"):
        budget = st.number_input(
            "Monthly budget",
            min_value=0.0,
            value=current_budget,
            step=500.0,
        )
        submitted = st.form_submit_button("Save Budget")

    if submitted:
        set_budget(user_id, month_key, budget)
        st.success("Budget saved successfully.")
        st.rerun()

    data = get_transactions(
        user_id,
        today.replace(day=1).isoformat(),
        today.isoformat(),
    )

    metrics = summary_metrics(data)
    status, percentage = budget_status(data, budget)

    st.write(
        f"**Status:** {status}  |  "
        f"**Used:** {percentage:.1f}%"
    )

    st.subheader("Monthly Trend")

    all_data = get_transactions(user_id)
    monthly = monthly_summary(all_data)

    if monthly.empty:
        st.info("Add transactions to see monthly trends.")
    else:
        chart_data = monthly.melt(
            id_vars="month",
            value_vars=["income", "expense"],
            var_name="type",
            value_name="amount",
        )

        chart = px.bar(
            chart_data,
            x="month",
            y="amount",
            color="type",
            barmode="group",
            title="Income vs Expenses",
        )
        st.plotly_chart(chart, use_container_width=True)

    st.subheader("Category Analysis")

    categories = category_summary(data)

    if categories.empty:
        st.info("No expense data available.")
    else:
        chart = px.bar(
            categories,
            x="category",
            y="amount",
            title="Expense by Category",
        )
        st.plotly_chart(chart, use_container_width=True)

    st.subheader("Monthly PDF Report")

    pdf_bytes = create_pdf(
        username,
        data,
        month_key,
        budget,
    )

    st.download_button(
        "Download Monthly PDF Report",
        data=pdf_bytes,
        file_name=f"expense_report_{month_key}.pdf",
        mime="application/pdf",
    )


if st.session_state.user is None:
    login_page()
else:
    dashboard_page()
