import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

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

def add_user(username, password):
    connection = get_connection()

    password_hash = generate_password_hash(password)

    connection.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )

    connection.commit()
    connection.close()

def verify_user(username, password):
  connection = get_connection()

  user=connection.execute("SELECT password_hash FROM users WHERE username= ?",
                          (username ,)).fetchone()
  connection.close()

  if user and check_password_hash(user[0],password):
      return True
  return False



if __name__ == "__main__":
    init_db()

