import hashlib
import sqlite3

from .database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(username, password):
    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    if len(password) < 4:
        return False, "Password must contain at least 4 characters."

    connection = get_connection()

    try:
        connection.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password)),
        )
        connection.commit()
        return True, "Registration successful. You can now log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        connection.close()


def login_user(username, password):
    connection = get_connection()

    row = connection.execute(
        "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
        (username.strip(), hash_password(password)),
    ).fetchone()

    connection.close()

    if row:
        return {"id": row["id"], "username": row["username"]}

    return None
