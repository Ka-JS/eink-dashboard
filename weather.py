# weather.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_weather():
    """
    Retrieves the current weather data from the OpenWeatherMap API.
    Returns:
    dict: A dictionary containing the temperature and weather condition description.
    """

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
    data = response.json()

    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    high = data["main"]["temp_max"]
    low = data["main"]["temp_min"]
    rain = data.get("rain", {}).get("1h", 0)  # Get rain volume for the last hour, default to 0 if not available

    return {
    "temp": temperature,
    "condition": description,
    "high": high,
    "low": low,
    "rain": rain
    }

if __name__ == "__main__": print(get_weather())