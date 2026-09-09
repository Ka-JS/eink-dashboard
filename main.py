# main.py
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from weather import get_weather
from calendar_api import get_calendar_events
from render import render_frame
from dotenv import load_dotenv
from brief import generate_brief

load_dotenv()

timezone_name = os.getenv("TIMEZONE") or "UTC"

tz = ZoneInfo(timezone_name)
now = datetime.now(tz)
start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0)

weather = get_weather()
events = get_calendar_events(
    calendar_id=os.getenv("GOOGLE_CALENDAR_ID"),
    start_of_day=start_of_day,
    end_of_day=end_of_day
)

brief = generate_brief(weather, events)

frame = render_frame(weather, events, brief)

print("Weather:", weather["condition"], "with a temperature of", weather["temp"], "°C")
print("Brief:", brief)
if not events:
    print("No events today.")
else:
    for event in events:
        print(event["start"], "-", event["title"])


frame.save("test.png")