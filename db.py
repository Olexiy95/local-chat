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

    def close(self):
        self.conn.close()

    def insert_user(self, username, password, email, name, bio, profile_picture=None):
        user_id = str(uuid.uuid4())
        self.cur.execute(
            "INSERT INTO users (id, username, password, email, name, bio, profile_picture) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, password, email, name, bio, profile_picture),
        )
        self.conn.commit()
        # self.conn.close()

    def update_user(
        self, user_id, username, password, email, name, bio, profile_picture
    ):
        if username:
            self.cur.execute(
                "UPDATE users SET username = ? WHERE id = ?", (username, user_id)
            )
        if password:
            self.cur.execute(
                "UPDATE users SET password = ? WHERE id = ?", (password, user_id)
            )
        if email:
            self.cur.execute(
                "UPDATE users SET email = ? WHERE id = ?", (email, user_id)
            )
        if name:
            self.cur.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
        if bio:
            self.cur.execute("UPDATE users SET bio = ? WHERE id = ?", (bio, user_id))
        if profile_picture:
            self.cur.execute(
                "UPDATE users SET profile_picture = ? WHERE id = ?",
                (profile_picture, user_id),
            )
        self.conn.commit()
        # self.conn.close()

    def get_user(self, user_id):
        self.cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = self.cur.fetchone()
        self.conn.commit()
        # self.conn.close()
        return user

    def insert_message(self, user_id, content):
        print("inserting message")
        message_id = generate_short_id()
        self.cur.execute(
            "INSERT INTO messages (id, user_id, content) VALUES (?, ?, ?)",
            (message_id, user_id, content),
        )
        self.conn.commit()
        # self.conn.close()

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
        # self.conn.close()
        return last_message

    def get_chat(self):
        self.cur.execute("SELECT * FROM chat")
        chat = self.cur.fetchall()
        self.conn.commit()
        # self.conn.close()
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
    with open("init.sql") as f:
        cursor.executescript(f.read())
    # TODO: Add admin user
    # hashed_password = bcrypt.hash("password")
    # cursor.execute(
    #     """
    #         INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)
    #     """,
    #     ("admin", hashed_password),
    # )

    conn.commit()
    conn.close()
