# main.py
import os
from datetime import datetime, timezone
from weather import get_weather
from calendar_api import get_calendar_events
from render import render_frame
from dotenv import load_dotenv

load_dotenv()

weather = get_weather()
events = get_calendar_events(
    calendar_id=os.getenv("GOOGLE_CALENDAR_ID"),
    start_of_day=datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0),
    end_of_day=datetime.now(timezone.utc).replace(hour=23, minute=59, second=59, microsecond=0)
)

frame = render_frame(weather, events)

print("Weather:", weather["condition"], "with a temperature of", weather["temp"], "°C")
if not events:
    print("No events today.")
else:
    for event in events:
        print(event["start"], "-", event["title"])

frame.save("test.png")