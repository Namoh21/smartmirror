"""
Fetches today's events from Google Calendar using OAuth2.

First-run setup:
  1. Go to https://console.cloud.google.com/ and create a project.
  2. Enable the Google Calendar API.
  3. Create OAuth2 credentials (Desktop app) and download as
     credentials/google_credentials.json
  4. Run `python -m src.services.calendar_service` once to complete the
     browser-based OAuth flow; a token is saved to credentials/google_token.json
     and reused on subsequent runs.
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def _get_credentials(credentials_file: Path, token_file: Path) -> Credentials | None:
    creds = None

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as exc:
                print(f"[calendar] token refresh failed: {exc}")
                creds = None

        if not creds:
            if not credentials_file.exists():
                print(
                    f"[calendar] credentials file not found: {credentials_file}\n"
                    "  See src/services/calendar_service.py for setup instructions."
                )
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES
            )
            creds = flow.run_local_server(port=0)

        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_file.write_text(creds.to_json())

    return creds


def fetch_todays_events(
    credentials_file: Path,
    token_file: Path,
    calendar_ids: str = "primary",
    max_results: int = 10,
) -> list[dict] | None:
    """
    Returns a list of event dicts for today, sorted by start time:
      {title, start, end, all_day, location}
    Returns None on auth failure; empty list if no events.
    """
    creds = _get_credentials(credentials_file, token_file)
    if creds is None:
        return None

    try:
        service = build("calendar", "v3", credentials=creds)
    except Exception as exc:
        print(f"[calendar] service build error: {exc}")
        return None

    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    end_of_day = (now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)).isoformat()

    events = []
    for cal_id in [c.strip() for c in calendar_ids.split(",")]:
        try:
            result = (
                service.events()
                .list(
                    calendarId=cal_id,
                    timeMin=start_of_day,
                    timeMax=end_of_day,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            for item in result.get("items", []):
                start_raw = item["start"].get("dateTime") or item["start"].get("date")
                end_raw = item["end"].get("dateTime") or item["end"].get("date")
                all_day = "dateTime" not in item["start"]

                if all_day:
                    start_fmt = "All day"
                    end_fmt = ""
                else:
                    try:
                        dt = datetime.fromisoformat(start_raw)
                        start_fmt = dt.strftime("%-I:%M %p")
                        dt_end = datetime.fromisoformat(end_raw)
                        end_fmt = dt_end.strftime("%-I:%M %p")
                    except Exception:
                        start_fmt = start_raw
                        end_fmt = end_raw

                events.append(
                    {
                        "title":    item.get("summary", "(No title)"),
                        "start":    start_fmt,
                        "end":      end_fmt,
                        "all_day":  all_day,
                        "location": item.get("location", ""),
                    }
                )
        except HttpError as exc:
            print(f"[calendar] API error for {cal_id}: {exc}")

    events.sort(key=lambda e: (e["all_day"], e["start"]))
    return events


# ---------------------------------------------------------------------------
# Run standalone to trigger first-time OAuth flow
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from src.config import GOOGLE_CREDENTIALS_FILE, GOOGLE_TOKEN_FILE, CALENDAR_IDS

    evts = fetch_todays_events(GOOGLE_CREDENTIALS_FILE, GOOGLE_TOKEN_FILE, CALENDAR_IDS)
    if evts is None:
        print("Auth failed — check setup instructions above.")
        sys.exit(1)
    if not evts:
        print("No events today.")
    for e in evts:
        time_str = e["start"] if e["all_day"] else f"{e['start']} – {e['end']}"
        print(f"  {time_str}  {e['title']}")
