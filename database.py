import sqlite3
from datetime import datetime

DB_NAME = "stock_signals.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock TEXT,
        decision TEXT,
        confidence INTEGER,
        price REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_signal(stock, decision, confidence, price):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO signals (stock, decision, confidence, price, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (stock, decision, confidence, price, datetime.now()))

    conn.commit()
    conn.close()

def fetch_signals():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM signals ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()

    conn.close()
    return rows