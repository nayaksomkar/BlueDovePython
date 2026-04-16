"""
Main tracker - monitors active windows and records usage.
Saves to SQLite database when you switch windows.
"""

import sys
import time
import datetime as dt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from win32gui import GetForegroundWindow, GetWindowText

from src.utils import date_cv, app_name, format_timestamp
from src.data_manager import data
from config.settings import APP_NAME, WINDOW_CHECK_INTERVAL, KEEP_DAYS


class ActivityTracker:
    def __init__(self):
        self.prev_window = ""
        self.prev_start = None
        self.today = date_cv(dt.date.today())

    def get_active_window(self):
        try:
            title = GetWindowText(GetForegroundWindow())
            return title, app_name(title)
        except Exception as e:
            print(f"[ERROR] {e}")
            return "", ""

    def save_window(self, window, app, start, end):
        # Calculate duration
        try:
            sh = int(start[11:13]) * 3600 + int(start[14:16]) * 60 + int(start[17:19])
            eh = int(end[11:13]) * 3600 + int(end[14:16]) * 60 + int(end[17:19])
            dur = eh - sh
            if dur < 0: dur = 0
        except: dur = 0

        hh, mm, ss = dur // 3600, (dur % 3600) // 60, dur % 60
        duration = f"{hh:02d}:{mm:02d}:{ss:02d}"

        try:
            data.add_record(self.today, app, window, duration, start, end)
            data.update_summary(self.today, app, hh, mm, ss)
            print(f"[SAVE] {app} - {duration}")
        except Exception as e:
            print(f"[ERROR] {e}")

    def track(self):
        print(f"{APP_NAME} - Activity Tracker")
        print("=" * 40)

        # Cleanup old data
        if KEEP_DAYS > 0:
            try:
                deleted = data.cleanup_old_data(KEEP_DAYS)
                if deleted: print(f"[CLEANUP] Removed {deleted} days")
            except Exception as e:
                print(f"[ERROR] {e}")

        print(f"Database: {data.db_path}")
        print(f"Press Ctrl+C to stop")
        print("=" * 40)

        self.prev_start = format_timestamp()

        try:
            while True:
                window, app = self.get_active_window()

                if window != self.prev_window:
                    now = format_timestamp()

                    # Save previous window
                    if self.prev_window:
                        self.save_window(self.prev_window, app_name(self.prev_window),
                                       self.prev_start, now)

                    self.prev_window = window
                    self.prev_start = now

                    # New day check
                    today = date_cv(dt.date.today())
                    if today != self.today:
                        self.today = today
                        print(f"[INFO] New day: {self.today}")

                time.sleep(WINDOW_CHECK_INTERVAL)

        except KeyboardInterrupt:
            if self.prev_window:
                self.save_window(self.prev_window, app_name(self.prev_window),
                               self.prev_start, format_timestamp())
            print("\nStopped.")

def main():
    tracker = ActivityTracker()
    tracker.track()

if __name__ == "__main__":
    main()
