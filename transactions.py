import pandas as pd

from .database import get_connection


EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Health",
    "Education",
    "Entertainment",
    "Rent",
    "Other",
]

INCOME_CATEGORIES = [
    "Salary",
    "Freelance",
    "Business",
    "Investment",
    "Other",
]


def add_transaction(user_id, transaction_type, amount, category, description, transaction_date):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO transactions
        (user_id, transaction_type, amount, category, description, transaction_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            transaction_type,
            float(amount),
            category,
            description.strip(),
            transaction_date,
        ),
    )

    connection.commit()
    connection.close()


def get_transactions(user_id, start_date=None, end_date=None):
    connection = get_connection()

    query = """
        SELECT id, transaction_type, amount, category,
               description, transaction_date
        FROM transactions
        WHERE user_id = ?
    """
    params = [user_id]

    if start_date:
        query += " AND transaction_date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND transaction_date <= ?"
        params.append(end_date)

    query += " ORDER BY transaction_date DESC, id DESC"

    dataframe = pd.read_sql_query(query, connection, params=params)
    connection.close()

    return dataframe


def update_transaction(
    transaction_id,
    user_id,
    transaction_type,
    amount,
    category,
    description,
    transaction_date,
):
    connection = get_connection()

    connection.execute(
        """
        UPDATE transactions
        SET transaction_type = ?, amount = ?, category = ?,
            description = ?, transaction_date = ?
        WHERE id = ? AND user_id = ?
        """,
        (
            transaction_type,
            float(amount),
            category,
            description.strip(),
            transaction_date,
            transaction_id,
            user_id,
        ),
    )

    connection.commit()
    connection.close()


def delete_transaction(transaction_id, user_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM transactions WHERE id = ? AND user_id = ?",
        (transaction_id, user_id),
    )

    connection.commit()
    connection.close()


def set_budget(user_id, month, amount):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO budgets (user_id, month, amount)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, month)
        DO UPDATE SET amount = excluded.amount
        """,
        (user_id, month, float(amount)),
    )

    connection.commit()
    connection.close()


def get_budget(user_id, month):
    connection = get_connection()

    row = connection.execute(
        "SELECT amount FROM budgets WHERE user_id = ? AND month = ?",
        (user_id, month),
    ).fetchone()

    connection.close()

    return float(row["amount"]) if row else 0.0
