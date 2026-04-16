# Blue Dove Settings

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

APP_NAME = "Blue Dove"
APP_VERSION = "2.0.0"

# How often to check active window (seconds) - 1 = every second
WINDOW_CHECK_INTERVAL = 1

# Max apps to show in charts
TOP_APPS_LIMIT = 6

# Auto-cleanup: keep only last X days (0 = keep all)
KEEP_DAYS = 10

# UI Colors
COLOR_PRIMARY = "#3498db"
COLOR_SECONDARY = "#2ecc71"
COLOR_BACKGROUND = "#ecf0f1"
COLOR_TEXT = "#2c3e50"
COLOR_ACCENT = "#e74c3c"

PIE_COLORS = ["#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c"]
