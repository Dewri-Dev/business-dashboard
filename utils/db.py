import sqlite3

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        revenue REAL,
        expenses REAL,
        inventory_cost REAL,
        category TEXT
    )
    """)

    conn.commit()
    conn.close()