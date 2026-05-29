# SmartMirror

A Raspberry Pi-powered smart mirror that displays a clock, local weather, Google Calendar events, and a scrolling news ticker on a 7" screen mounted behind a full-length mirror. A light sensor automatically turns the display on and off based on room lighting.

![Layout](https://img.shields.io/badge/platform-Raspberry%20Pi-red) ![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- **Clock** — large live clock with date
- **Weather** — current conditions, feels-like, humidity, wind, and today's high/low via [Open-Meteo](https://open-meteo.com/) (free, no API key)
- **Google Calendar** — today's events pulled from your family calendar
- **News ticker** — scrolling bottom bar with local, US, and world headlines via RSS
- **Light sensor** — automatically turns the display on/off based on room light (GPIO + LDR)
- **Auto-start** — runs on boot via systemd

---

## Hardware Required

| Part | Notes |
|------|-------|
| Raspberry Pi 4 (or 3B+) | Any model with GPIO headers |
| Official 7" Raspberry Pi touchscreen | 800×480, connects via DSI ribbon |
| Full-length mirror with backing removed | Two-way mirror acrylic works well |
| LDR (photoresistor) | Standard 5mm GL5528 or similar |
| 10 kΩ resistor | Pull-down for LDR voltage divider |
| Jumper wires | GPIO → breadboard |

### Light Sensor Wiring

```
3.3V ──[LDR]──┬── GPIO 4
               │
            [10kΩ]
               │
             GND
```

The GPIO pin is configurable in `.env` (`SM_GPIO_PIN`). To skip the sensor entirely, set `SM_LIGHT_SENSOR=false`.

---

## Installation

### 1. Prerequisites

Ensure your Raspberry Pi is running **Raspberry Pi OS (64-bit)** with a desktop environment and Python 3.10+.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv python3-tk git -y
```

### 2. Clone the repository

```bash
git clone https://github.com/Namoh21/smartmirror.git
cd smartmirror
```

### 3. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gpiozero RPi.GPIO   # Raspberry Pi GPIO support
```

### 4. Configure your settings

```bash
cp .env.example .env
nano .env
```

Key settings to update:

| Variable | Description | Example |
|----------|-------------|---------|
| `SM_LATITUDE` | Your latitude | `41.8781` |
| `SM_LONGITUDE` | Your longitude | `-87.6298` |
| `SM_CITY` | City name shown on display | `Chicago` |
| `SM_TIMEZONE` | IANA timezone name | `America/Chicago` |
| `SM_LOCAL_NEWS_RSS` | RSS URL for your local news source | see `.env.example` |
| `SM_GPIO_PIN` | GPIO pin number for light sensor | `4` |
| `SM_LIGHT_SENSOR` | Enable/disable light sensor | `true` |

Load your `.env` before running:

```bash
export $(cat .env | xargs)
```

### 5. Connect Google Calendar

1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
2. Enable the **Google Calendar API**.
3. Navigate to **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
   - Application type: **Desktop app**
4. Download the JSON file and save it to:
   ```
   credentials/google_credentials.json
   ```
5. Run the one-time authorisation flow (this opens a browser):
   ```bash
   python -m src.services.calendar_service
   ```
   A token is saved to `credentials/google_token.json` and reused automatically on every subsequent start.

> **Family calendar tip:** Find your calendar's ID under Google Calendar Settings → *[Calendar name]* → Integrate calendar → **Calendar ID**. Set `SM_CALENDAR_IDS=<id>` in your `.env`.

### 6. Run the mirror

```bash
python -m src.main
```

Press **Escape** or **q** to exit.

### 7. Auto-start on boot (optional)

```bash
sudo cp smartmirror.service /etc/systemd/system/
```

Open the service file and update the `User` and `WorkingDirectory` paths if your username is not `pi`:

```bash
sudo nano /etc/systemd/system/smartmirror.service
```

Then enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable smartmirror
sudo systemctl start smartmirror
```

Check status with `sudo systemctl status smartmirror`.

---

## Display Layout

```
┌────────────────────────────────────────┐
│              12:34 PM                  │
│         Friday, May 29 2026            │
├──────────────────┬─────────────────────┤
│  WEATHER         │  TODAY              │
│  Chicago         │  8:00 AM  School    │
│  ☀️  72°F        │  12:00 PM Dentist   │
│  Clear sky       │  6:00 PM  Dinner    │
│  Feels like 70°  │                     │
│  High 78° Low 61°│                     │
├──────────────────┴─────────────────────┤
│ LOCAL: ... ◆ US: ... ◆ WORLD: ...  ←scrolling
└────────────────────────────────────────┘
```

---

## Troubleshooting

**Display won't turn on/off with the sensor**
Run `vcgencmd display_power 1` manually to confirm the command works on your Pi. Check your wiring and that `SM_GPIO_PIN` matches your actual wiring.

**Calendar shows "not connected"**
Re-run `python -m src.services.calendar_service` to redo the OAuth flow. Make sure `credentials/google_credentials.json` exists.

**News ticker shows "Loading news…" indefinitely**
Check that your `SM_LOCAL_NEWS_RSS` URL is valid and reachable from the Pi. US and world feeds use BBC and NPR RSS which are public.

**App crashes on startup**
Ensure `python3-tk` is installed (`sudo apt install python3-tk`) and that you are running in a desktop session (not headless SSH without `DISPLAY` set).

---

## Disclaimer

> **USE AT YOUR OWN RISK.**
>
> This project is provided for personal, educational, and hobbyist use only. The author(s) make no representations or warranties of any kind, express or implied, regarding the safety, reliability, accuracy, or fitness for any particular purpose of this software or the hardware instructions provided.
>
> By using this project you acknowledge and agree that:
>
> - Any physical build involving mirrors, glass, electrical components, or wall mounting carries inherent risk of property damage or personal injury.
> - The author(s) are **not responsible** for any damage to hardware, property, data, or any injury to persons arising from the use, misuse, or inability to use this software or the associated hardware instructions.
> - You are solely responsible for ensuring your build complies with all applicable local electrical codes, safety regulations, and best practices.
> - Google Calendar integration requires granting OAuth access to your Google account. Review Google's own terms and privacy policy before authorising.
>
> This software is distributed "as is", without warranty of any kind. Use it responsibly.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
