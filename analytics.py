import pandas as pd


def summary_metrics(dataframe):
    if dataframe.empty:
        return {
            "income": 0.0,
            "expense": 0.0,
            "savings": 0.0,
        }

    income = dataframe.loc[
        dataframe["transaction_type"] == "Income", "amount"
    ].sum()

    expense = dataframe.loc[
        dataframe["transaction_type"] == "Expense", "amount"
    ].sum()

    return {
        "income": float(income),
        "expense": float(expense),
        "savings": float(income - expense),
    }


def category_summary(dataframe):
    if dataframe.empty:
        return pd.DataFrame(columns=["category", "amount"])

    expenses = dataframe[dataframe["transaction_type"] == "Expense"].copy()

    if expenses.empty:
        return pd.DataFrame(columns=["category", "amount"])

    return (
        expenses.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )


def monthly_summary(dataframe):
    if dataframe.empty:
        return pd.DataFrame(columns=["month", "income", "expense"])

    data = dataframe.copy()
    data["transaction_date"] = pd.to_datetime(data["transaction_date"])
    data["month"] = data["transaction_date"].dt.to_period("M").astype(str)

    income = (
        data[data["transaction_type"] == "Income"]
        .groupby("month")["amount"]
        .sum()
        .rename("income")
    )

    expense = (
        data[data["transaction_type"] == "Expense"]
        .groupby("month")["amount"]
        .sum()
        .rename("expense")
    )

    result = pd.concat([income, expense], axis=1).fillna(0).reset_index()
    return result.sort_values("month")


def budget_status(dataframe, budget):
    metrics = summary_metrics(dataframe)
    expense = metrics["expense"]

    if budget <= 0:
        return "No budget set", 0.0

    percentage = (expense / budget) * 100

    if percentage > 100:
        status = "Budget exceeded"
    elif percentage >= 80:
        status = "Close to budget"
    else:
        status = "Within budget"

    return status, percentage
