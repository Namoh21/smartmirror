"""
Fetches current weather and today's hourly forecast from Open-Meteo (free, no key).
https://open-meteo.com/
"""

import requests
from datetime import datetime, date

BASE_URL = "https://api.open-meteo.com/v1/forecast"

# WMO weather interpretation codes → human-readable label + emoji
WMO_CODES = {
    0:  ("Clear sky", "☀️"),
    1:  ("Mainly clear", "🌤️"),
    2:  ("Partly cloudy", "⛅"),
    3:  ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Icy fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Drizzle", "🌦️"),
    55: ("Heavy drizzle", "🌧️"),
    61: ("Light rain", "🌧️"),
    63: ("Rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    71: ("Light snow", "🌨️"),
    73: ("Snow", "❄️"),
    75: ("Heavy snow", "❄️"),
    77: ("Snow grains", "🌨️"),
    80: ("Rain showers", "🌦️"),
    81: ("Showers", "🌧️"),
    82: ("Violent showers", "⛈️"),
    85: ("Snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm + hail", "⛈️"),
    99: ("Thunderstorm + hail", "⛈️"),
}


def _wmo(code: int) -> tuple[str, str]:
    return WMO_CODES.get(code, ("Unknown", "❓"))


def fetch_weather(lat: float, lon: float, timezone: str = "auto") -> dict | None:
    """
    Returns a dict with keys:
      current: {temp_f, feels_like_f, condition, icon, humidity, wind_mph}
      today:   {high_f, low_f, condition, icon}
    Returns None on failure.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": timezone,
        "current": [
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "wind_speed_10m",
            "weather_code",
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "weather_code",
        ],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "forecast_days": 1,
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        print(f"[weather] fetch error: {exc}")
        return None

    cur = data.get("current", {})
    daily = data.get("daily", {})

    cur_code = cur.get("weather_code", 0)
    day_code = (daily.get("weather_code") or [0])[0]
    cur_label, cur_icon = _wmo(cur_code)
    day_label, day_icon = _wmo(day_code)

    return {
        "current": {
            "temp_f":       round(cur.get("temperature_2m", 0)),
            "feels_like_f": round(cur.get("apparent_temperature", 0)),
            "humidity":     cur.get("relative_humidity_2m", 0),
            "wind_mph":     round(cur.get("wind_speed_10m", 0)),
            "condition":    cur_label,
            "icon":         cur_icon,
        },
        "today": {
            "high_f":    round((daily.get("temperature_2m_max") or [0])[0]),
            "low_f":     round((daily.get("temperature_2m_min") or [0])[0]),
            "condition": day_label,
            "icon":      day_icon,
        },
        "fetched_at": datetime.now().isoformat(),
    }
