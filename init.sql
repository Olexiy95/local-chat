CREATE TABLE
    IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        bio TEXT,
        profile_picture BLOB,
        is_admin BOOLEAN DEFAULT FALSE
    );

CREATE TABLE
    IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id TEXT NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );

CREATE VIEW
    IF NOT EXISTS chat AS
SELECT
    messages.timestamp,
    users.username,
    messages.content,
    user.id
FROM
    messages
    JOIN users ON messages.user_id = users.id
ORDER BY
    messages.timestamp;