import sqlite3 as sqlite


DB_NAME = "example.db"

conn = sqlite.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS ad
    (
        creator_id INTEGER,
        ad_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        desc TEXT NOT NULL,
        price REAL,
        date TEXT NOT NULL,
        is_available INTEGER,
        buyer INTEGER
    )
''')
conn.commit()

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS user
    (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        address TEXT NOT NULL,
        phone_number TEXT NOT NULL UNIQUE
    )
''')
conn.commit()

class SQLite(object):

    def __enter__(self):
        self.conn = sqlite.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
