"""
Data Manager - handles SQLite database operations.
Stores usage data in two tables:
- usage: individual window sessions
- summary: aggregated time per app per day
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "usage.db"


class DataManager:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    # Create tables if not exist
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    app TEXT NOT NULL,
                    window TEXT,
                    duration TEXT,
                    start_time TEXT,
                    end_time TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS summary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    app TEXT NOT NULL,
                    hours INTEGER DEFAULT 0,
                    minutes INTEGER DEFAULT 0,
                    seconds INTEGER DEFAULT 0,
                    UNIQUE(date, app)
                )
            """)

    # Add a single window session
    def add_record(self, date: str, app: str, window: str,
                   duration: str, start: str, end: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO usage (date, app, window, duration, start_time, end_time)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (date, app, window, duration, start, end))

    # Update total time for an app (adds to existing)
    def update_summary(self, date: str, app: str,
                       hours: int, minutes: int, seconds: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("""
                SELECT hours, minutes, seconds FROM summary WHERE date = ? AND app = ?
            """, (date, app))

            row = cur.fetchone()
            if row:
                # Add to existing
                total = row[0] * 3600 + row[1] * 60 + row[2]
                total += hours * 3600 + minutes * 60 + seconds
                h, m, s = total // 3600, (total % 3600) // 60, total % 60
                conn.execute("""
                    UPDATE summary SET hours = ?, minutes = ?, seconds = ?
                    WHERE date = ? AND app = ?
                """, (h, m, s, date, app))
            else:
                # Create new
                conn.execute("""
                    INSERT INTO summary (date, app, hours, minutes, seconds)
                    VALUES (?, ?, ?, ?, ?)
                """, (date, app, hours, minutes, seconds))

    # Get summary for a date
    def get_summary(self, date: str) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("""
                SELECT app, hours, minutes, seconds FROM summary WHERE date = ?
            """, (date,))
            return [{"app": row[0], "seconds": row[1]*3600 + row[2]*60 + row[3]}
                    for row in cur.fetchall()]

    # Get all sessions for a date
    def get_records(self, date: str) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("""
                SELECT app, window, duration, start_time, end_time
                FROM usage WHERE date = ? ORDER BY id
            """, (date,))
            return [{"app": r[0], "window": r[1], "duration": r[2],
                     "start": r[3], "end": r[4]} for r in cur.fetchall()]

    # Get all dates with data
    def get_dates(self) -> List[str]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT DISTINCT date FROM summary ORDER BY date DESC")
            return [row[0] for row in cur.fetchall()]

    # Delete old data
    def cleanup_old_data(self, keep_days: int = 10) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT DISTINCT date FROM summary ORDER BY date DESC")
            all_dates = [row[0] for row in cur.fetchall()]

            if len(all_dates) <= keep_days:
                return 0

            old = all_dates[keep_days:]
            placeholders = ','.join('?' * len(old))
            conn.execute(f"DELETE FROM usage WHERE date IN ({placeholders})", old)
            conn.execute(f"DELETE FROM summary WHERE date IN ({placeholders})", old)
            return len(old)


# Global instance
data = DataManager()
