# SmartMirror Setup Guide

## 1. Clone and install

```bash
git clone <your-repo> smartmirror
cd smartmirror
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Raspberry Pi only
pip install gpiozero RPi.GPIO
```

## 2. Configure location and news

```bash
cp .env.example .env
# Edit .env — set your latitude/longitude, city, timezone, and local news RSS URL
```

Load the env before running:
```bash
export $(cat .env | xargs)         # Linux/Pi
# Windows: set each variable manually or use a .env loader
```

## 3. Connect Google Calendar

1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create a project.
2. Enable the **Google Calendar API**.
3. Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
   - Application type: **Desktop app**
4. Download the JSON file and save it as `credentials/google_credentials.json`.
5. Run the one-time auth flow (opens a browser):
   ```bash
   python -m src.services.calendar_service
   ```
   A `credentials/google_token.json` is saved; the mirror uses it silently from then on.

**Tip:** To use the family calendar specifically, find the calendar's ID in Google Calendar
settings (Settings → [calendar name] → Integrate calendar → Calendar ID) and set
`SM_CALENDAR_IDS=<id>` in your `.env`.

## 4. Wire the light sensor

Use a standard LDR (photoresistor) with a 10 kΩ pull-down resistor:

```
3.3V ──[LDR]──┬── GPIO 4
               │
            [10kΩ]
               │
             GND
```

The pin is configurable via `SM_GPIO_PIN` in `.env`.  
To disable the sensor entirely, set `SM_LIGHT_SENSOR=false`.

## 5. Run

```bash
python -m src.main
```

Press **Escape** or **q** to quit.

## 6. Auto-start on boot (Raspberry Pi)

```bash
sudo cp smartmirror.service /etc/systemd/system/
# Edit the service file if your username isn't "pi" or your path differs
sudo systemctl daemon-reload
sudo systemctl enable smartmirror
sudo systemctl start smartmirror
```

## Layout

```
┌────────────────────────────────────────┐
│              12:34 PM                  │  ← clock
│         Friday, May 29 2026            │
├──────────────────┬─────────────────────┤
│  WEATHER         │  TODAY              │  ← weather (left)
│  Chicago         │  8:00 AM  School    │    calendar (right)
│  ☀️  72°F        │  12:00 PM Dentist   │
│  Clear sky       │  6:00 PM  Dinner    │
│  Feels like 70°  │                     │
│  High 78° Low 61°│                     │
├──────────────────┴─────────────────────┤
│ LOCAL: ... ◆ US: ... ◆ WORLD: ...  ←scrolling ticker
└────────────────────────────────────────┘
```
