import sqlite3
from datetime import datetime

# =========================================
# INIT DATABASE
# =========================================

def init_db():

    conn = sqlite3.connect("database/attendance.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()

# =========================================
# SAVE ATTENDANCE
# =========================================

def save_attendance(name):

    conn = sqlite3.connect("database/attendance.db")

    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    # =====================================
    # CHECK IF ALREADY EXISTS TODAY
    # =====================================

    cursor.execute("""
    SELECT * FROM attendance
    WHERE name=? AND date=?
    """, (name, current_date))

    existing = cursor.fetchone()

    # =====================================
    # INSERT ONLY ONCE
    # =====================================

    if existing is None:

        cursor.execute("""
        INSERT INTO attendance (name, date, time)
        VALUES (?, ?, ?)
        """, (name, current_date, current_time))

        conn.commit()

    conn.close()