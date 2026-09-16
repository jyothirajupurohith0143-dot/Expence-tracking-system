import streamlit as st
import pandas as pd
from io import BytesIO

from .transactions import get_transactions


def render_reports(user_id):
    st.title("📊 Expense Reports")

    transactions = get_transactions(user_id)

    if transactions.empty:
        st.info("No transactions available to generate a report.")
        return

    st.subheader("Transaction Summary")

    total_income = transactions[
        transactions["transaction_type"] == "Income"
    ]["amount"].sum()

    total_expense = transactions[
        transactions["transaction_type"] == "Expense"
    ]["amount"].sum()

    savings = total_income - total_expense

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Income", f"₹{total_income:,.2f}")
    col2.metric("Total Expenses", f"₹{total_expense:,.2f}")
    col3.metric("Savings", f"₹{savings:,.2f}")

    st.divider()

    st.subheader("All Transactions")

    st.dataframe(
        transactions,
        use_container_width=True
    )

    st.divider()

    st.subheader("📥 Download Report")

    csv_data = transactions.to_csv(index=False)

    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="expense_report.csv",
        mime="text/csv"
    )
