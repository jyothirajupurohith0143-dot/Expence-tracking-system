import streamlit as st
from datetime import date

from .transactions import set_budget, get_budget, get_transactions


def render_budget(user_id):
    st.title("💰 Monthly Budget")

    selected_date = st.date_input(
        "Select Month",
        value=date.today()
    )

    month = selected_date.strftime("%Y-%m")

    current_budget = get_budget(user_id, month)

    st.subheader(f"Budget for {month}")

    budget_amount = st.number_input(
        "Monthly Budget Amount",
        min_value=0.0,
        value=float(current_budget),
        step=500.0
    )

    if st.button("Save Budget"):
        set_budget(user_id, month, budget_amount)
        st.success("Budget saved successfully!")
        st.rerun()

    transactions = get_transactions(user_id)

    if not transactions.empty:
        transactions["transaction_date"] = transactions[
            "transaction_date"
        ].astype(str)

        monthly_expenses = transactions[
            (transactions["transaction_type"] == "Expense")
            & (
                transactions["transaction_date"].str.startswith(month)
            )
        ]["amount"].sum()
    else:
        monthly_expenses = 0.0

    remaining = budget_amount - monthly_expenses

    col1, col2, col3 = st.columns(3)

    col1.metric("Monthly Budget", f"₹{budget_amount:,.2f}")
    col2.metric("Total Expenses", f"₹{monthly_expenses:,.2f}")
    col3.metric("Remaining", f"₹{remaining:,.2f}")

    if budget_amount > 0:
        percentage = (monthly_expenses / budget_amount) * 100

        st.progress(min(percentage / 100, 1.0))

        st.write(f"Budget Used: **{percentage:.1f}%**")

        if percentage >= 100:
            st.error("⚠️ You have exceeded your monthly budget.")
        elif percentage >= 80:
            st.warning("⚠️ You have used more than 80% of your budget.")
        else:
            st.success("✅ You are within your budget.")
