 # render.py
from datetime import datetime
import os
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont
import textwrap

timezone_name = os.getenv("TIMEZONE") or "UTC"


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
        return start_time.strftime("%H:%M")
    else:
        return "All day"

def shorten_title(title, max_chars=25): # 25 because of the available space in the display
    """Shortens a title to fit the display, adding an ellipsis if necessary."""
    if len(title) > max_chars:
        return title[:max_chars - 1].rstrip() + "…"
    return title

def render_frame(weather, events, brief):
    """Renders the entire frame for the e-ink display."""
    img = Image.new("RGB", (800, 480), "white")
    draw = ImageDraw.Draw(img)

    # Fonts
    time_font = ImageFont.truetype("fonts/InterDisplay-Bold.ttf", 64)
    header_font = ImageFont.truetype("fonts/InterDisplay-Bold.ttf", 18)
    temp_font = ImageFont.truetype("fonts/InterDisplay-Bold.ttf", 40)
    label_font = ImageFont.truetype("fonts/Inter.ttf", 22)
    small_font = ImageFont.truetype("fonts/Inter.ttf", 16)
    weather_font = ImageFont.truetype("fonts/weathericons.ttf", 44)

    now = datetime.now(ZoneInfo(timezone_name))

    if weather["is_day"]:
        icon_char = WEATHER_ICONS.get(weather["main"], WEATHER_ICONS["Clear"])["day"]
    else:
        icon_char = WEATHER_ICONS.get(weather["main"], WEATHER_ICONS["Clear"])["night"]

    # left column
    draw.text((24, 24), now.strftime("%H:%M"), font=time_font, fill="black")
    draw.text((24, 102), now.strftime("%A, %d %B"), font=label_font, fill="black")
    
    # Weather
    draw.text((24, 150), icon_char, font=weather_font, fill="black")
    draw.text((74, 150), f"{int(weather['temp'])}°C", font=temp_font, fill="black")
    
    draw.text((24, 205), weather["condition"].capitalize(), font=small_font, fill="#444444")
    draw.text((24, 227), f"H:{int(weather['high'])}°   L:{int(weather['low'])}°", font=small_font, fill="#444444")

    if weather["rain"] > 0:
        draw.text((24, 249), f"Rain: {weather['rain']}mm/h", font=small_font, fill="#444444")

    # right column
    draw.text((428, 24), "TODAY", font=header_font, fill="black")
    draw.line([(428, 50), (780, 50)], fill="black", width=1)

    # today events
    event_y = 68
    if not events:
        draw.text((428, event_y), "Nothing scheduled.", font=label_font, fill="#666666")
    else:
        MAX_EVENTS_SHOWN = 5
        displayed = events[:MAX_EVENTS_SHOWN]
        remaining = len(events) - len(displayed)

        for event in displayed:
            draw.text((428, event_y), format_event_time(event), font=label_font, fill="black")
            draw.text((490, event_y), f"· {shorten_title(event['title'])}", font=label_font, fill="black")
            event_y += 34

        if remaining > 0:
            draw.text((428, event_y), f"+{remaining} more", font=small_font, fill="#666666")

    # lines to separate sections
    draw.line([(400, 24), (400, 260)], fill="black", width=2)
    draw.line([(24, 280), (780, 280)], fill="black", width=2)

    # brief
    draw.text((24, 295), "BRIEF", font=header_font, fill="black")
    
    brief_y = (332-5)
    for line in textwrap.wrap(brief, width=70):
        draw.text((24, brief_y), line, font=label_font, fill="black")
        brief_y += 28

    return img