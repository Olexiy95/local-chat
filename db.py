import sqlite3
from config import CHAT_DATABASE_NAME
from passlib.hash import bcrypt
import uuid
from utils import generate_short_id


class DatabaseManager:
    def __init__(self, database_name: str):
        print("DatabaseManager init")
        self.conn = sqlite3.connect(database_name, check_same_thread=False)
        print("DatabaseManager conn:", self.conn)
        self.cur = self.conn.cursor()

    def insert_user(self, username, password, email, name, bio, profile_picture=None):
        user_id = str(uuid.uuid4())
        self.cur.execute(
            "INSERT INTO users (id, username, password, email, name, bio, profile_picture) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, password, email, name, bio, profile_picture),
        )
        self.conn.commit()
        self.conn.close()

    def insert_message(self, user_id, content):
        message_id = generate_short_id()
        self.cur.execute(
            "INSERT INTO messages (id, user_id, content) VALUES (?, ?, ?)",
            (message_id, user_id, content),
        )
        self.conn.commit()
        self.conn.close()

    def get_last_message(self, user_id):
        self.cur.execute(
                        """
                        SELECT * FROM chat 
                        WHERE timestamp = (
                            SELECT MAX(timestamp) 
                            FROM messages 
                            WHERE user_id = ?
                        )
                        """,
                        (user_id,),
                    )
        last_message = self.cur.fetchone()
        self.conn.commit()
        self.conn.close()
        return last_message


    def get_chat(self):
        self.cur.execute("SELECT * FROM chat")
        chat = self.cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return chat



def get_db(db_name=CHAT_DATABASE_NAME):
    conn = sqlite3.connect(db_name, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()


def init_db(db_name=CHAT_DATABASE_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            bio TEXT,
            profile_picture TEXT,
            is_admin BOOLEAN DEFAULT FALSE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE VIEW IF NOT EXISTS chat AS SELECT 
        messages.timestamp, users.username, messages.content
        FROM messages
        JOIN users ON messages.user_id = users.id
        ORDER BY messages.timestamp
        """
    )
    hashed_password = bcrypt.hash("password")
    cursor.execute(
        """
            INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)
        """,
        ("admin", hashed_password),
    )

    conn.commit()
    conn.close()
