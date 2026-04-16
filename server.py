"""
Server - serves dashboard and provides API.
Endpoints:
- / -> dashboard
- /api/info -> database info
- /api/dates -> list of dates
- /api/use/<db> -> switch database
- /api/data/<date> -> usage data for date
"""

import http.server
import socketserver
import json
import sqlite3
from pathlib import Path
from typing import Optional

PORT = 8000
BASE_DIR = Path(__file__).parent
UI_DIR = BASE_DIR / "ui"
DATA_DIR = BASE_DIR / "data"

DB_MAIN: Path = DATA_DIR / "usage.db"
DB_SAMPLE: Path = DATA_DIR / "sample_usage.db"


class BlueDoveServer:
    def __init__(self):
        self.current_db: Path = DB_SAMPLE

    def use_db(self, db_name: str) -> None:
        self.current_db = DB_SAMPLE if db_name == "sample" else DB_MAIN

    def get_dates(self) -> list:
        if not self.current_db.exists():
            return []
        conn = sqlite3.connect(str(self.current_db))
        try:
            cur = conn.execute("SELECT DISTINCT date FROM summary ORDER BY date DESC")
            return [row[0] for row in cur.fetchall()]
        finally:
            conn.close()

    def get_usage(self, date: str) -> dict:
        result = {"summary": [], "records": []}
        if not self.current_db.exists():
            return result

        conn = sqlite3.connect(str(self.current_db))
        try:
            # Get summary (hours, mins, secs -> total seconds)
            cur = conn.execute(
                "SELECT app, hours, minutes, seconds FROM summary WHERE date = ?",
                (date,)
            )
            for row in cur.fetchall():
                total = row[1] * 3600 + row[2] * 60 + row[3]
                result["summary"].append({"app": row[0], "seconds": total})

            # Get individual records
            cur = conn.execute(
                "SELECT app, window, duration, start_time, end_time FROM usage WHERE date = ? ORDER BY id",
                (date,)
            )
            for row in cur.fetchall():
                result["records"].append({
                    "app": str(row[0]) if row[0] else "",
                    "window": str(row[1]) if row[1] else "",
                    "duration": str(row[2]) if row[2] else "00:00:00",
                    "start": str(row[3]) if row[3] else "",
                    "end": str(row[4]) if row[4] else ""
                })
        finally:
            conn.close()

        return result

    def get_info(self) -> dict:
        return {
            "current": "sample" if self.current_db == DB_SAMPLE else "main",
            "sample_exists": DB_SAMPLE.exists(),
            "main_exists": DB_MAIN.exists()
        }


server = BlueDoveServer()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def send_json(self, data: dict) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self) -> None:
        try:
            if self.path == "/":
                self.path = "/index.html"
                super().do_GET()
            elif self.path == "/api/info":
                self.send_json(server.get_info())
            elif self.path == "/api/dates":
                self.send_json(server.get_dates())
            elif self.path.startswith("/api/use/"):
                db = self.path.split("/")[-1]
                server.use_db(db)
                self.send_json({"dates": server.get_dates()})
            elif self.path.startswith("/api/data/"):
                date = self.path.split("/")[-1]
                self.send_json(server.get_usage(date))
            else:
                super().do_GET()
        except Exception as e:
            print("[ERROR]", e)
            self.send_error(500)

    def log_message(self, format: str, *args) -> None:
        print(f"[{self.log_date_time_string()}] {args[0]}")


if __name__ == "__main__":
    print("=" * 40)
    print("Blue Dove Dashboard")
    print("Open: http://localhost:8000")
    print("=" * 40)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
