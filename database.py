import sqlite3

def get_connection():
    connection  = sqlite3.connect("book_discovery.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS user_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_key TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Want to Read',
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE (book_key, user_id)
        )
    """)

    connection.commit()
    connection.close()



if __name__ == "__main__":
    init_db()

