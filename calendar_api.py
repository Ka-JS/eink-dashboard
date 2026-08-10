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

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])

    clean_events = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        clean_events.append({
            "title": event.get("summary", "Untitled"),
            "start": start,
            "end": end,
            "location": event.get("location", None)
        })
        
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

    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created_event


if __name__ == "__main__":
    calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
    now = datetime.now()
    start = now.replace(hour=15, minute=0, second=0, microsecond=0)
    end = now.replace(hour=16, minute=0, second=0, microsecond=0)

    result = create_calendar_event(calendar_id, {
        "title": "Test Event",
        "start": start.isoformat(),
        "end": end.isoformat(),
    })
    print(result)