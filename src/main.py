"""
SmartMirror — entry point.
Run: python -m src.main
"""

import tkinter as tk
import threading
from src import config
from src.widgets.clock_widget import ClockWidget
from src.widgets.weather_widget import WeatherWidget
from src.widgets.calendar_widget import CalendarWidget
from src.widgets.news_ticker import NewsTicker
from src.services.light_sensor import LightSensor


class SmartMirrorApp:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("SmartMirror")
        self._root.configure(bg=config.BG_COLOR)
        self._root.resizable(False, False)

        if config.FULLSCREEN:
            self._root.attributes("-fullscreen", True)
            self._root.attributes("-topmost", True)
        else:
            self._root.geometry(f"{config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}")

        # Press Escape or q to quit (handy during dev)
        self._root.bind("<Escape>", lambda _: self._shutdown())
        self._root.bind("q", lambda _: self._shutdown())

        self._sensor = LightSensor(
            gpio_pin=config.LIGHT_SENSOR_GPIO_PIN,
            enabled=config.LIGHT_SENSOR_ENABLED,
        )

        self._build_layout()
        self._start_light_monitor()

    def _build_layout(self):
        root = self._root

        # ── Top: clock centred ──────────────────────────────────────────────
        clock_frame = tk.Frame(root, bg=config.BG_COLOR)
        clock_frame.pack(fill="x", pady=(20, 10))
        ClockWidget(clock_frame).pack(anchor="center")

        # ── Middle: weather left, calendar right ────────────────────────────
        mid = tk.Frame(root, bg=config.BG_COLOR)
        mid.pack(fill="both", expand=True, padx=30, pady=10)

        WeatherWidget(mid).pack(side="left", anchor="n", padx=(0, 40))

        # Vertical divider
        tk.Frame(mid, bg=config.FG_DIM, width=1).pack(
            side="left", fill="y", padx=10
        )

        CalendarWidget(mid).pack(side="left", anchor="n", fill="both", expand=True)

        # ── Bottom: scrolling news ticker ───────────────────────────────────
        NewsTicker(root).pack(side="bottom", fill="x")

    def _start_light_monitor(self):
        def _monitor():
            self._sensor.update_display()
            self._root.after(
                config.LIGHT_CHECK_INTERVAL_SECONDS * 1000, _monitor
            )

        self._root.after(config.LIGHT_CHECK_INTERVAL_SECONDS * 1000, _monitor)

    def _shutdown(self):
        self._sensor.close()
        self._root.destroy()

    def run(self):
        self._root.mainloop()


def main():
    SmartMirrorApp().run()


if __name__ == "__main__":
    main()
