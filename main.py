from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (800, 480), "white")
draw = ImageDraw.Draw(img)

time_font = ImageFont.truetype("fonts/InterDisplay-Bold.ttf", 64)
label_font = ImageFont.truetype("fonts/Inter.ttf", 22)
weather_font = ImageFont.truetype("fonts/weathericons.ttf", 48)

now = datetime.now()
draw.text((20, 20), now.strftime("%H:%M"), fill="black", font=time_font)
draw.text((20, 100), now.strftime("%A, %d %B %Y"), fill="black", font=label_font)

draw.text((600, 20), "\uf019", fill="black", font=weather_font)

img.save("test.png")