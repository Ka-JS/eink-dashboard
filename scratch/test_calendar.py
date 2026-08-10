from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone
import os

#This file is entirely for testing the Google Calendar API, and is not used in the main program. It is kept here for reference.

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


calendar_id = "..."

now = datetime.now(timezone.utc)
start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0)

events_result = service.events().list(
    calendarId=calendar_id,
    timeMin=start_of_day.isoformat(),
    timeMax=end_of_day.isoformat(),
    singleEvents=True,
    orderBy="startTime",
).execute()

events = events_result.get("items", [])

if not events:
    print("No events today.")
else:
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, "-", event["summary"])