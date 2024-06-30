import sqlite3
from config import CHAT_DATABASE_NAME
from passlib.hash import bcrypt
import uuid
from utils import generate_short_id


class DatabaseManager:
    def __init__(self, database_name: str):
        self.database_name = database_name
        print("DatabaseManager init")
        # self.conn = sqlite3.connect(database_name, check_same_thread=False)
        print("DatabaseManager conn:")
        # self.cur = self.conn.cursor()

    def _execute_query(self, query, params=None, commit=False):
        with sqlite3.connect(self.database_name, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            try:
                cursor.execute(query, params or ())
                if commit:
                    conn.commit()
                if cursor.description:  # Check if the query returns data
                    fetched_data = cursor.fetchall()
                    if len(fetched_data) == 1:
                        return [dict(row) for row in fetched_data][0]
                        # return fetched_data
                    else:
                        return [dict(row) for row in fetched_data]
            except Exception as e:
                conn.rollback()
                print(f"Database error during query execution: {e}")
                raise e

    # def _execute_query(self, query, params=None, commit=False):
    #     with sqlite3.connect(self.database_name, check_same_thread=False) as conn:
    #         # Set the row factory to sqlite3.Row
    #         conn.row_factory = sqlite3.Row

    #         cursor = conn.cursor()
    #         try:
    #             cursor.execute(query, params or ())
    #             if commit:
    #                 conn.commit()
    #             if cursor.description:  # Check if the query returns data
    #                 fetched_data = cursor.fetchall()
    #                 # Convert fetched rows to dictionaries if there is data
    #                 if fetched_data:
    #                     return [dict(row) for row in fetched_data]
    #         except Exception as e:
    #             conn.rollback()
    #             print(f"Database error during query execution: {e}")
    #             raise e
    # def close(self):
    #     self.conn.close()

    # def rollback(self):
    #     self.conn.rollback()

    def insert_user(self, username, password, email, name, bio, profile_picture=None):
        user_id = str(uuid.uuid4())
        query = "INSERT INTO users (id, username, password, email, name, bio, profile_picture)"
        params = (user_id, username, password, email, name, bio, profile_picture)
        self._execute_query(query, params, commit=True)

    def update_user(
        self, user_id, username, password, email, name, bio, profile_picture
    ):
        updates = []
        params = []
        if username:
            updates.append("username = ?")
            params.append(username)
        if password:
            updates.append("password = ?")
            params.append(password)
        if email:
            updates.append("email = ?")
            params.append(email)
        if name:
            updates.append("name = ?")
            params.append(name)
        if bio:
            updates.append("bio = ?")
            params.append(bio)
        if profile_picture:
            updates.append("profile_picture = ?")
            params.append(profile_picture)

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        self._execute_query(query, params, commit=True)

    def get_user(self, user_id):
        query = "SELECT * FROM users WHERE id = ?"
        return self._execute_query(query, (user_id,))

    def insert_message(self, user_id, content):
        message_id = generate_short_id()
        query = "INSERT INTO messages (id, user_id, content) VALUES (?, ?, ?)"
        self._execute_query(query, (message_id, user_id, content), commit=True)

    def get_last_message(self, user_id):
        query = """
            SELECT * FROM chat WHERE timestamp = (
                SELECT MAX(timestamp) FROM messages WHERE user_id = ?
            )
        """
        return self._execute_query(query, (user_id,))

    def get_chat(self):
        return self._execute_query("SELECT * FROM chat")


def get_db():
    conn = sqlite3.connect(CHAT_DATABASE_NAME, check_same_thread=False)
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
