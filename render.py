# render.py
from datetime import datetime
import os
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont

WEATHER_ICONS = {
    "Clear": {"day": "\uf00d", "night": "\uf02e"},
    "Clouds": {"day": "\uf002", "night": "\uf086"},
    "Rain": {"day": "\uf019", "night": "\uf019"},
    "Drizzle": {"day": "\uf01a", "night": "\uf01a"},
    "Thunderstorm": {"day": "\uf01e", "night": "\uf01e"},
    "Snow": {"day": "\uf01b", "night": "\uf01b"},
    "Mist": {"day": "\uf021", "night": "\uf021"},
    "Fog": {"day": "\uf021", "night": "\uf021"},
    "Haze": {"day": "\uf0b6", "night": "\uf0b6"},
}

def format_event_time(event):
    """Formats the event time for display."""
    start = event["start"]
    end = event["end"]
    if "T" in start:
        start_time = datetime.fromisoformat(start)
        end_time = datetime.fromisoformat(end)
        duration = end_time - start_time
        if duration.total_seconds() <= 3600:  # If the event is less than an hour, show only the start time
            return start_time.strftime("%H:%M")
        else:
            return f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
    else:
        return "All day"

def render_frame(weather, events):
    """Renders the frame with the current time, weather, and calendar events."""
    img = Image.new("RGB", (800, 480), "white")
    draw = ImageDraw.Draw(img)

    time_font = ImageFont.truetype("fonts/InterDisplay-Bold.ttf", 64)
    label_font = ImageFont.truetype("fonts/Inter.ttf", 22)
    weather_font = ImageFont.truetype("fonts/weathericons.ttf", 48)
    condition = WEATHER_ICONS.get(weather["main"], WEATHER_ICONS["Clear"])
    icon_char = condition["day"] if weather["is_day"] else condition["night"]

    timezone_name = os.getenv("TIMEZONE") or "UTC"
    draw.text((20, 20), datetime.now(ZoneInfo(timezone_name)).strftime("%H:%M"), font=time_font, fill="black")
    draw.text((20, 100), f"Weather: {weather['condition']}, {weather['temp']}°C", font=label_font, fill="black")
    draw.text((500, 20), icon_char, font=weather_font, fill="black")
    y = 180
    for event in events:
        time_str = format_event_time(event)
        draw.text((20, y), time_str, font=label_font, fill="black")
        draw.text((150, y), f" ·  {event['title']}", font=label_font, fill="black")  # fixed x, always same column
        y += 30  # move down for the next line

    return img