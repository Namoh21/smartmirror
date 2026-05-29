"""
Light sensor control using a digital LDR wired to a GPIO pin.

Hardware: wire an LDR (photoresistor) and a 10kΩ pull-down resistor between
GPIO_PIN and GND.  When light > threshold the pin reads HIGH.

On non-Pi systems the sensor is mocked (always "light").

Display power is controlled via:
  vcgencmd display_power 1   (on)
  vcgencmd display_power 0   (off)
"""

import subprocess
import sys


def _is_raspberry_pi() -> bool:
    try:
        with open("/proc/cpuinfo") as f:
            return "Raspberry Pi" in f.read()
    except OSError:
        return False


IS_PI = _is_raspberry_pi()


class LightSensor:
    def __init__(self, gpio_pin: int, enabled: bool = True):
        self._pin = gpio_pin
        self._enabled = enabled and IS_PI
        self._display_on = True
        self._sensor = None

        if self._enabled:
            try:
                from gpiozero import LightSensor as _GPIOLightSensor
                # charge_time_limit controls sensitivity; tune to your LDR
                self._sensor = _GPIOLightSensor(gpio_pin, charge_time_limit=0.01)
                print(f"[light] GPIO light sensor initialised on pin {gpio_pin}")
            except Exception as exc:
                print(f"[light] GPIO init failed, running without sensor: {exc}")
                self._enabled = False

    def is_light(self) -> bool:
        """Return True when ambient light is detected."""
        if not self._enabled or self._sensor is None:
            return True  # mock: always lit
        try:
            return self._sensor.light_detected
        except Exception:
            return True

    def update_display(self) -> None:
        """Turn display on/off based on light level (only on Pi)."""
        if not IS_PI:
            return
        should_be_on = self.is_light()
        if should_be_on == self._display_on:
            return
        self._display_on = should_be_on
        power = 1 if should_be_on else 0
        try:
            subprocess.run(
                ["vcgencmd", "display_power", str(power)],
                check=True,
                capture_output=True,
            )
            state = "ON" if should_be_on else "OFF"
            print(f"[light] display turned {state}")
        except Exception as exc:
            print(f"[light] display_power error: {exc}")

    def close(self) -> None:
        if self._sensor is not None:
            try:
                self._sensor.close()
            except Exception:
                pass
