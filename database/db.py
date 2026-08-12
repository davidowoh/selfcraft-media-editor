import sqlite3
import os

os.makedirs("database", exist_ok=True)
DB_PATH = "database/sme.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filepath TEXT UNIQUE,
            programme TEXT,
            week TEXT,
            module TEXT,
            lesson_number TEXT,
            lesson_title TEXT,
            status TEXT DEFAULT 'detected',
            date_added TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_video(filepath, metadata):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR IGNORE INTO videos (filepath, programme, week, module, lesson_number, lesson_title) VALUES (?,?,?,?,?,?)",
        (filepath, metadata.get('programme'), metadata.get('week'),
         metadata.get('module'), metadata.get('lesson_number'), metadata.get('lesson_title'))
    )
    conn.commit()
    conn.close()

def get_all_videos():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM videos ORDER BY date_added DESC").fetchall()
    conn.close()
    return rows