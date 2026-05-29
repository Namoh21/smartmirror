"""Displays today's Google Calendar events."""

import tkinter as tk
from src import config
from src.services import calendar_service

MAX_EVENTS_SHOWN = 8


class CalendarWidget(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=config.BG_COLOR, **kwargs)
        self._event_frames: list[tk.Frame] = []
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        tk.Label(
            self, text="TODAY", font=config.FONT_SECTION_HEADER,
            fg=config.FG_ACCENT, bg=config.BG_COLOR,
        ).pack(anchor="w")

        self._list_frame = tk.Frame(self, bg=config.BG_COLOR)
        self._list_frame.pack(anchor="w", fill="x")

    def _refresh(self):
        for f in self._event_frames:
            f.destroy()
        self._event_frames.clear()

        events = calendar_service.fetch_todays_events(
            config.GOOGLE_CREDENTIALS_FILE,
            config.GOOGLE_TOKEN_FILE,
            config.CALENDAR_IDS,
        )

        if events is None:
            self._add_row("⚠️", "Calendar not connected", config.FG_DIM)
        elif not events:
            self._add_row("", "No events today", config.FG_DIM)
        else:
            for evt in events[:MAX_EVENTS_SHOWN]:
                time_str = evt["start"] if evt["all_day"] else f"{evt['start']}"
                self._add_row(time_str, evt["title"])

        self.after(config.CALENDAR_REFRESH_SECONDS * 1000, self._refresh)

    def _add_row(self, time_str: str, title: str, color: str = None):
        color = color or config.FG_PRIMARY
        row = tk.Frame(self._list_frame, bg=config.BG_COLOR)
        row.pack(anchor="w", fill="x", pady=1)

        tk.Label(
            row, text=time_str, font=config.FONT_SMALL,
            fg=config.FG_ACCENT, bg=config.BG_COLOR, width=10, anchor="w",
        ).pack(side="left")

        tk.Label(
            row, text=title, font=config.FONT_SMALL,
            fg=color, bg=config.BG_COLOR, anchor="w",
        ).pack(side="left")

        self._event_frames.append(row)
