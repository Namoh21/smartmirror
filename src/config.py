"""
Central configuration — edit this file before first run.
Copy .env.example to .env for secrets, or set values directly here.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Location (used for weather)
# ---------------------------------------------------------------------------
LATITUDE = float(os.getenv("SM_LATITUDE", "41.8781"))   # default: Chicago
LONGITUDE = float(os.getenv("SM_LONGITUDE", "-87.6298"))
CITY_NAME = os.getenv("SM_CITY", "Chicago")
TIMEZONE = os.getenv("SM_TIMEZONE", "America/Chicago")  # IANA tz name

# ---------------------------------------------------------------------------
# Weather (Open-Meteo — free, no API key required)
# ---------------------------------------------------------------------------
WEATHER_REFRESH_SECONDS = 600   # 10 minutes

# ---------------------------------------------------------------------------
# Google Calendar
# ---------------------------------------------------------------------------
GOOGLE_CREDENTIALS_FILE = BASE_DIR / "credentials" / "google_credentials.json"
GOOGLE_TOKEN_FILE = BASE_DIR / "credentials" / "google_token.json"
# Comma-separated calendar IDs; "primary" = the account's main calendar
CALENDAR_IDS = os.getenv("SM_CALENDAR_IDS", "primary")
CALENDAR_REFRESH_SECONDS = 300  # 5 minutes

# ---------------------------------------------------------------------------
# News (RSS feeds — free, no API key)
# ---------------------------------------------------------------------------
NEWS_FEEDS = {
    "local": os.getenv(
        "SM_LOCAL_NEWS_RSS",
        "https://feeds.feedburner.com/chicagotribune/news",  # replace with your local paper
    ),
    "us": "https://feeds.npr.org/1001/rss.xml",
    "world": "https://feeds.bbci.co.uk/news/world/rss.xml",
}
NEWS_HEADLINES_PER_FEED = 5       # headlines pulled from each feed
NEWS_REFRESH_SECONDS = 900        # 15 minutes
NEWS_SCROLL_SPEED_MS = 30         # lower = faster ticker scroll

# ---------------------------------------------------------------------------
# Light sensor (Raspberry Pi GPIO)
# ---------------------------------------------------------------------------
LIGHT_SENSOR_ENABLED = os.getenv("SM_LIGHT_SENSOR", "true").lower() == "true"
LIGHT_SENSOR_GPIO_PIN = int(os.getenv("SM_GPIO_PIN", "4"))
LIGHT_CHECK_INTERVAL_SECONDS = 5

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
FULLSCREEN = os.getenv("SM_FULLSCREEN", "true").lower() == "true"
SCREEN_WIDTH = int(os.getenv("SM_WIDTH", "800"))
SCREEN_HEIGHT = int(os.getenv("SM_HEIGHT", "480"))  # Pi 7" official display

# ---------------------------------------------------------------------------
# UI colours / fonts
# ---------------------------------------------------------------------------
BG_COLOR = "#000000"
FG_PRIMARY = "#FFFFFF"
FG_DIM = "#AAAAAA"
FG_ACCENT = "#7EC8E3"   # light blue accent

FONT_CLOCK = ("Helvetica", 96, "bold")
FONT_DATE = ("Helvetica", 22)
FONT_SECTION_HEADER = ("Helvetica", 14, "bold")
FONT_BODY = ("Helvetica", 13)
FONT_SMALL = ("Helvetica", 11)
FONT_TICKER = ("Helvetica", 13)
