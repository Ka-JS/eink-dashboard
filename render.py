from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


def render_frame(weather, events):
    """Renders the frame with the current time, weather, and calendar events."""
    img = Image.new("RGB", (800, 480), "white")
    draw = ImageDraw.Draw(img)

    time_font = ImageFont.truetype("fonts/InterDisplay-Bold.ttf", 64)
    label_font = ImageFont.truetype("fonts/Inter.ttf", 22)
    weather_font = ImageFont.truetype("fonts/weathericons.ttf", 48)

    draw.text((20, 20), datetime.now().strftime("%H:%M"), font=time_font, fill="black")
    draw.text((20, 100), f"Weather: {weather['condition']}, {weather['temp']}°C", font=label_font, fill="black")
    y = 180
    for event in events:
        draw.text((20, y), f"{event['start']} - {event['title']}", font=label_font, fill="black")
        y += 30  # move down for the next line

    return img