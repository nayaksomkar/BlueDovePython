"""
Generate sample database with realistic developer usage data.
Run: python create_sample_db.py
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import random

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_DB = DATA_DIR / "sample_usage.db"

# Popular developer apps
APPS = [
    {"name": "Visual Studio Code", "weight": 35},  # Main coding
    {"name": "Chrome", "weight": 20},              # Research/docs
    {"name": "Discord", "weight": 10},             # Communication
    {"name": "Telegram", "weight": 8},            # Messaging
    {"name": "File Explorer", "weight": 7},        # File management
    {"name": "Terminal", "weight": 5},            # Command line
    {"name": "Spotify", "weight": 5},              # Music
    {"name": "Far Cry 4", "weight": 4},           # Gaming
    {"name": "Notepad", "weight": 3},             # Quick notes
    {"name": "GitHub Desktop", "weight": 3},      # Version control
]


def create_sample_db():
    """Create sample database with 10 days of data."""
    SAMPLE_DB.parent.mkdir(parents=True, exist_ok=True)

    # Remove existing sample db
    if SAMPLE_DB.exists():
        SAMPLE_DB.unlink()

    conn = sqlite3.connect(SAMPLE_DB)
    conn.execute("""
        CREATE TABLE usage (
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
        CREATE TABLE summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            app TEXT NOT NULL,
            hours INTEGER DEFAULT 0,
            minutes INTEGER DEFAULT 0,
            seconds INTEGER DEFAULT 0,
            UNIQUE(date, app)
        )
    """)

    # Generate 10 days of data
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%b%d%y").upper()
             for i in range(10)]

    for date in dates:
        # Total screen time: 14-17 hours per day
        total_seconds = random.randint(14 * 3600, 17 * 3600)
        remaining = total_seconds

        for app in APPS:
            if remaining <= 0:
                break

            # Weight-based allocation
            weight = app["weight"]
            app_seconds = int((weight / 100) * total_seconds)
            app_seconds = min(app_seconds, remaining)
            remaining -= app_seconds

            if app_seconds < 60:
                continue

            # Split into multiple sessions
            num_sessions = random.randint(2, 6)
            session_len = app_seconds // num_sessions

            base_hour = random.randint(8, 10)  # Start day around 8-10 AM

            for i in range(num_sessions):
                # Random session length
                s_len = session_len + random.randint(-300, 300)
                if s_len < 60:
                    s_len = 60

                start_hour = base_hour + (i * 2) + random.randint(0, 1)
                if start_hour >= 24:
                    start_hour = start_hour % 24

                start_min = random.randint(0, 59)
                start = f"{date.lower()[3:5]}-{date.lower()[:2]}-{20+int(date[5])} {start_hour:02d}:{start_min:02d}:00"

                end_sec = s_len
                end_min = start_min + (s_len // 60)
                end_h = start_hour + (end_min // 60)
                end_m = end_min % 60
                end = f"{start[:11]}{end_h:02d}:{end_m:02d}:{s_len % 60:02d}"

                # Format duration
                hh = s_len // 3600
                mm = (s_len % 3600) // 60
                ss = s_len % 60
                duration = f"{hh:02d}:{mm:02d}:{ss:02d}"

                window_title = f"{app['name']} - Project"

                conn.execute("""
                    INSERT INTO usage (date, app, window, duration, start_time, end_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (date, app["name"], window_title, duration, start, end))

                # Update summary
                conn.execute("""
                    INSERT INTO summary (date, app, hours, minutes, seconds)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(date, app) DO UPDATE SET
                        hours = hours + excluded.hours,
                        minutes = minutes + excluded.minutes,
                        seconds = seconds + excluded.seconds
                """, (date, app["name"], hh, mm, ss))

    conn.commit()
    conn.close()

    print(f"Created sample database: {SAMPLE_DB}")
    print(f"Dates: {dates[0]} to {dates[-1]}")
    print(f"Total screen time per day: 14-17 hours")


if __name__ == "__main__":
    create_sample_db()
