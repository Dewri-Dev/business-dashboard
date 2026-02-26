import sqlite3
import os

DB_NAME = "database.db"

def get_connection():
    """Returns a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initializes the database by wiping old data and creating fresh tables."""
    
    # --- NEW: Automatically delete the old database file if it exists ---
    if os.path.exists(DB_NAME):
        try:
            os.remove(DB_NAME)
            print("Old database wiped. Starting fresh!")
        except PermissionError:
            print("Could not delete DB. It might be open in another program.")
    # --------------------------------------------------------------------

    conn = get_connection()
    cursor = conn.cursor()

    # Create the fresh table
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

def insert_record(date, revenue, expenses, inventory_cost, category="General"):
    """Inserts a new financial record into the database."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO business_data (date, revenue, expenses, inventory_cost, category)
    VALUES (?, ?, ?, ?, ?)
    """, (date, revenue, expenses, inventory_cost, category))

    conn.commit()
    conn.close()

def get_all_records():
    """Retrieves all records from the database."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT date, revenue, expenses, inventory_cost, category FROM business_data ORDER BY date ASC")
    rows = cur.fetchall()

    conn.close()
    return rows

# Create/Initialize table automatically when the module is imported
init_db()