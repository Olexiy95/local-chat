import sqlite3
from config import CHAT_DATABASE_NAME
from passlib.hash import bcrypt


def init_db():
    conn = sqlite3.connect(CHAT_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id REFERENCES users(id),
            content TEXT NOT NULL
        )
    """
    )
    cursor.execute(
        """
        CREATE VIEW IF NOT EXISTS chat AS
        SELECT messages.timestamp, users.username, messages.content
        FROM messages
        JOIN users ON messages.user_id = users.id
        ORDER BY messages.timestamp
    """
    )
    hashed_password = bcrypt.hash("password")  # Replace with actual password
    cursor.execute(
        """
        INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)
        """,
        ("admin", hashed_password),
    )

    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect(CHAT_DATABASE_NAME, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()
