# calendar_api.py
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

def get_calendar_events(calendar_id, start_of_day, end_of_day):
    """Fetches events from the specified Google Calendar for the given day."""

    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    clean_events = []
    
    for cid in calendar_id.split(","):
        try:
            events_result = service.events().list(
                calendarId=cid.strip(),
                timeMin=start_of_day.isoformat(),
                timeMax=end_of_day.isoformat(),
                singleEvents=True,
                orderBy="startTime",
                timeZone=os.getenv("TIMEZONE")
            ).execute()

            events = events_result.get("items", [])

            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))
                clean_events.append({
                    "title": event.get("summary", "Untitled"),
                    "start": start,
                    "end": end,
                    "location": event.get("location", None)
                })
        except Exception:
            pass

    clean_events.sort(key=lambda x: x["start"])
    return clean_events


def create_calendar_event(calendar_id, event_dict):
    """Creates a new event in the specified Google Calendar."""

    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    event = {
    "summary": event_dict["title"],
    "start": {
        "dateTime": event_dict["start"],
        "timeZone": os.getenv("TIMEZONE"),
    },
    "end": {
        "dateTime": event_dict["end"],
        "timeZone": os.getenv("TIMEZONE"),
    },
}

    primary_id = calendar_id.split(",")[0].strip()
    created_event = service.events().insert(calendarId=primary_id, body=event).execute()
    return created_event


if __name__ == "__main__":
    calendar_id = os.getenv("GOOGLE_CALENDAR_IDS") # used to add events to calendar for testing
    now = datetime.now()
    start = now.replace(hour=10, minute=0, second=0, microsecond=0)
    end = now.replace(hour=12, minute=0, second=0, microsecond=0)

    result = create_calendar_event(calendar_id, {
        "title": "DATA.ML.100, Tekoälyn perusteet, Luennot",
        "start": start.isoformat(),
        "end": end.isoformat(),
    })
    print(result)