# Blue Dove - PC Activity Tracker

Tracks which apps you use and for how long.

**Windows only**

## Preview

![Dashboard Preview 1](BDpreview1.png)

![Dashboard Preview 2](BDpreview2.png)

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
# Terminal 1: Start tracking
python src/main.py

# Terminal 2: Start dashboard
python server.py
```

Open browser: http://localhost:8000

## Sample Data

```bash
python create_sample_db.py
```

## Files

| File | Purpose |
|------|---------|
| `src/main.py` | Tracks active windows |
| `server.py` | Dashboard server |
| `src/data_manager.py` | SQLite storage |
| `src/utils.py` | Helper functions |
| `ui/index.html` | Dashboard UI |
| `data/` | SQLite databases |

## Settings

Edit `config/settings.py`:
- `WINDOW_CHECK_INTERVAL` - Seconds between checks (default: 1)
- `KEEP_DAYS` - Days of data to keep (default: 10)

## Requirements

- Python 3.8+
- Windows (uses win32gui)
- pywin32
