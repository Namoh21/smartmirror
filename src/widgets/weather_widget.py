"""Displays current conditions and today's high/low."""

import tkinter as tk
from src import config
from src.services import weather_service


class WeatherWidget(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=config.BG_COLOR, **kwargs)
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        # Section header
        tk.Label(
            self, text="WEATHER", font=config.FONT_SECTION_HEADER,
            fg=config.FG_ACCENT, bg=config.BG_COLOR,
        ).pack(anchor="w")

        tk.Label(
            self, text=config.CITY_NAME, font=config.FONT_SMALL,
            fg=config.FG_DIM, bg=config.BG_COLOR,
        ).pack(anchor="w")

        self._icon_temp = tk.Label(
            self, text="—", font=("Helvetica", 48, "bold"),
            fg=config.FG_PRIMARY, bg=config.BG_COLOR,
        )
        self._icon_temp.pack(anchor="w")

        self._condition = tk.Label(
            self, text="", font=config.FONT_BODY,
            fg=config.FG_DIM, bg=config.BG_COLOR,
        )
        self._condition.pack(anchor="w")

        self._details = tk.Label(
            self, text="", font=config.FONT_SMALL,
            fg=config.FG_DIM, bg=config.BG_COLOR,
        )
        self._details.pack(anchor="w")

        self._high_low = tk.Label(
            self, text="", font=config.FONT_SMALL,
            fg=config.FG_DIM, bg=config.BG_COLOR,
        )
        self._high_low.pack(anchor="w")

    def _refresh(self):
        data = weather_service.fetch_weather(
            config.LATITUDE, config.LONGITUDE, config.TIMEZONE
        )
        if data:
            cur = data["current"]
            tod = data["today"]
            self._icon_temp.config(
                text=f"{cur['icon']}  {cur['temp_f']}°F"
            )
            self._condition.config(text=cur["condition"])
            self._details.config(
                text=f"Feels like {cur['feels_like_f']}°  ·  "
                     f"Humidity {cur['humidity']}%  ·  "
                     f"Wind {cur['wind_mph']} mph"
            )
            self._high_low.config(
                text=f"High {tod['high_f']}°  ·  Low {tod['low_f']}°"
            )
        else:
            self._icon_temp.config(text="—")
            self._condition.config(text="Unable to fetch weather")

        self.after(config.WEATHER_REFRESH_SECONDS * 1000, self._refresh)
