"""
Helper functions for Blue Dove.
"""

from typing import Tuple, List, Optional
from datetime import datetime


# Convert date: 2026-04-16 -> APR1606
def date_cv(acc_date) -> str:
    acc_date = str(acc_date).split("-")
    months = {"01": "JAN", "02": "FEB", "03": "MAR", "04": "APR",
              "05": "MAY", "06": "JUN", "07": "JUL", "08": "AUG",
              "09": "SEP", "10": "OCT", "11": "NOV", "12": "DEC"}
    if len(acc_date) >= 3 and acc_date[1] in months:
        return months[acc_date[1]] + acc_date[2] + acc_date[0][-2:]
    return ""


# Clean app name from window title
def app_name(full_name: str) -> str:
    result = "".join(c for c in full_name if c.isalpha() or c == " ")
    if "Telegram" in result:
        result = "Telegram"
    return result.replace("  ", " ").strip()


# Calculate time duration between two timestamps
def uss_time(s_time: str, e_time: str) -> Tuple[str, str, str, List[str]]:
    sh = int(s_time[11:13]) * 3600 + int(s_time[14:16]) * 60 + int(s_time[17:19])
    eh = int(e_time[11:13]) * 3600 + int(e_time[14:16]) * 60 + int(e_time[17:19])
    diff = eh - sh

    hh, mm, ss = diff // 3600, (diff % 3600) // 60, diff % 60
    formatted = f"{hh:02d}:{mm:02d}:{ss:02d}"
    return (s_time, e_time, formatted, [str(hh), str(mm), str(ss)])


# Format seconds to readable string
def format_time(seconds: int) -> str:
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    parts = []
    if h: parts.append(f"{h}h")
    if m: parts.append(f"{m}m")
    parts.append(f"{s}s")
    return " ".join(parts)


# Get current timestamp as string
def format_timestamp(dt_obj: Optional[datetime] = None) -> str:
    if dt_obj is None:
        dt_obj = datetime.now()
    return str(dt_obj)[:19]
