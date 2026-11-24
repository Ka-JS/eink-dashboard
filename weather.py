# weather.py
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo

load_dotenv()


def get_weather():
    """Retrieves the current weather data from the OpenWeatherMap API."""

    api_key = os.getenv("OPENWEATHER_API_KEY")
    lat = os.getenv("WEATHER_LAT")
    lon = os.getenv("WEATHER_LON")
    tz = ZoneInfo(os.getenv("TIMEZONE") or "UTC") #timevalues
    today = datetime.now(tz).strftime("%Y-%m-%d")
    

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
    }

    response = requests.get(url, params=params)
    data = response.json()

    #forecast (3h steps)
    forecast = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params).json()["list"]
    high = max(s["main"]["temp"] for s in forecast[:8])  #next 24h
    low = min(s["main"]["temp"] for s in forecast[:8])
    pop = round(max(s["pop"] for s in forecast[:8]) * 100)  #rain/snow
    hours = forecast[:4]  #next 12h
    days = []
    for s in forecast:
        if s["dt_txt"].endswith("12:00:00"):  #midday slot
            if not s["dt_txt"].startswith(today):  #skip today
                days.append(s)
    days = days[:3]  #next 3 days


    temperature = data["main"]["temp"]
    high = max(high, temperature) #to include now in output
    low = min(low, temperature)
    description = data["weather"][0]["description"]
    rain = data.get("rain", {}).get("1h", 0)  # Get rain volume for the last hour, default to 0 if not available
    main_condition = data["weather"][0]["main"]
    icon_code = data["weather"][0]["icon"]
    is_day = icon_code.endswith("d")
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], tz).strftime("%H:%M")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"], tz).strftime("%H:%M")

    return {
    "temp": temperature,
    "condition": description,
    "main": main_condition,
    "high": high,
    "low": low,
    "rain": rain,
    "is_day": is_day,
    "sunrise": sunrise,
    "sunset": sunset,
    "pop": pop,
    "hours": hours,
    "days": days
}



if __name__ == "__main__": print(get_weather())