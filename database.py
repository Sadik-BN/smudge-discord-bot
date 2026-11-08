import sqlite3

DATABASE_NAME = "smudge.db"


def initialize_database():
    connection = sqlite3.connect(DATABASE_NAME)

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'model')),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_user_time
            ON messages (user_id, created_at)
        """)

        connection.commit()

    finally:
        connection.close()


def save_message(user_id, role, content):
    connection = sqlite3.connect(DATABASE_NAME)

    try:
        connection.execute(
            """
            INSERT INTO messages (user_id, role, content)
            VALUES (?, ?, ?)
            """,
            (str(user_id), role, content)
        )

        connection.commit()

    finally:
        connection.close()


def get_messages(user_id, limit=20):
    connection = sqlite3.connect(DATABASE_NAME)

    try:
        cursor = connection.execute(
            """
            SELECT role, content
            FROM messages
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (str(user_id), limit)
        )

        messages = cursor.fetchall()
        messages.reverse()

        return messages

    finally:
        connection.close()

def delete_messages(user_id):
    connection = sqlite3.connect(DATABASE_NAME)

    try:
        connection.execute(
            """
            DELETE FROM messages
            WHERE user_id = ?
            """,
            (str(user_id),)
        )

        connection.commit()

    finally:
        connection.close()

def cleanup_expired_messages(retention_days):
    connection = sqlite3.connect(DATABASE_NAME)

    try:
        connection.execute(
            """
            DELETE FROM messages
            WHERE created_at < datetime('now', ?)
            """,
            (f"-{retention_days} days",)
        )

        connection.commit()

    finally:
        connection.close()