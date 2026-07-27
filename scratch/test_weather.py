import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
lat = os.getenv("WEATHER_LAT")
lon = os.getenv("WEATHER_LON")

url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
    "units": "metric",
}

response = requests.get(url, params=params)
print("Status code:", response.status_code)
print(response.json())