"""Large clock + date displayed at the top centre of the mirror."""

import tkinter as tk
from datetime import datetime
from src import config


class ClockWidget(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=config.BG_COLOR, **kwargs)

        self._time_var = tk.StringVar()
        self._date_var = tk.StringVar()

        tk.Label(
            self,
            textvariable=self._time_var,
            font=config.FONT_CLOCK,
            fg=config.FG_PRIMARY,
            bg=config.BG_COLOR,
        ).pack()

        tk.Label(
            self,
            textvariable=self._date_var,
            font=config.FONT_DATE,
            fg=config.FG_DIM,
            bg=config.BG_COLOR,
        ).pack()

        self._tick()

    def _tick(self):
        now = datetime.now()
        self._time_var.set(now.strftime("%I:%M %p").lstrip("0"))
        self._date_var.set(now.strftime("%A, %B %-d %Y"))
        self.after(1000, self._tick)
