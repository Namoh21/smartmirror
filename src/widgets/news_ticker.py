"""
Horizontally scrolling news ticker at the bottom of the screen.
Headlines are fetched in a background thread to avoid blocking the UI.
"""

import tkinter as tk
import threading
from src import config
from src.services import news_service

SEPARATOR = "    ◆    "


class NewsTicker(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=config.BG_COLOR, **kwargs)

        # Thin accent line above ticker
        tk.Frame(self, bg=config.FG_ACCENT, height=1).pack(fill="x")

        self._canvas = tk.Canvas(
            self,
            bg=config.BG_COLOR,
            highlightthickness=0,
            height=28,
        )
        self._canvas.pack(fill="x")

        self._text_id = None
        self._x = 0
        self._headline_str = "Loading news…"
        self._canvas.bind("<Configure>", self._on_resize)
        self._canvas_width = config.SCREEN_WIDTH

        self._draw_text()
        self._scroll()
        self._fetch_headlines()

    def _on_resize(self, event):
        self._canvas_width = event.width

    def _draw_text(self):
        if self._text_id is not None:
            self._canvas.delete(self._text_id)
        self._text_id = self._canvas.create_text(
            self._x, 14,
            text=self._headline_str,
            font=config.FONT_TICKER,
            fill=config.FG_PRIMARY,
            anchor="w",
        )

    def _scroll(self):
        self._x -= 1
        bbox = self._canvas.bbox(self._text_id)
        if bbox and bbox[2] < 0:
            # reset to just off right edge
            self._x = self._canvas_width + 10
        self._canvas.coords(self._text_id, self._x, 14)
        self.after(config.NEWS_SCROLL_SPEED_MS, self._scroll)

    def _fetch_headlines(self):
        def _worker():
            headlines = news_service.fetch_headlines(
                config.NEWS_FEEDS,
                config.NEWS_HEADLINES_PER_FEED,
            )
            if headlines:
                joined = SEPARATOR.join(headlines) + SEPARATOR
                # Update on main thread
                self.after(0, lambda: self._update_text(joined))

        threading.Thread(target=_worker, daemon=True).start()
        # Schedule next fetch
        self.after(config.NEWS_REFRESH_SECONDS * 1000, self._fetch_headlines)

    def _update_text(self, text: str):
        self._headline_str = text
        self._canvas.itemconfig(self._text_id, text=text)
