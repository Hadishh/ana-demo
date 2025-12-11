from bs4 import BeautifulSoup
import requests
from langchain.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_function
from datetime import datetime
import dateutil


def simple_weather_label(code: int) -> str:
    if code in {0, 1}:
        return "Sunny"
    if code in {2}:
        return "Partly cloudy"
    if code in {3}:
        return "Cloudy"
    if code in {45, 48}:
        return "Foggy"
    if code in {51, 53, 55, 56, 57}:
        return "Drizzle"
    if code in {61, 63, 65, 80, 81, 82}:
        return "Rainy"
    if code in {66, 67}:
        return "Freezing rain"
    if code in {71, 73, 75, 77, 85, 86}:
        return "Snowy"
    if code in {95, 96, 97}:
        return "Thunderstorm"
    return "Unknown"


@tool
async def get_weather(city_name: str, date_time: datetime):
    """
    Gets the weather information in a city of a given date and time.

    Parameters:
    ----------
    city_name: str
        The name of the city in which we require the weather information.

    date_time: datetime
        Date time of the requested time.

    Returns:
    -------
    str
        Weather information in details.
    """

    try:
        if type(date_time) == str:
            date_time = dateutil.parser.parse(date_time)
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": city_name, "count": 1}
        r = requests.get(url, params)
        data = r.json()

        if not data.get("results"):
            raise ValueError("City not found!")

        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,precipitation,weathercode",
            "start": date_time.isoformat(),
            "end": date_time.isoformat(),
        }
        r = requests.get(url, params=params)
        data = r.json()

        # Extract hourly result
        hourly = data.get("hourly", {})
        if not hourly:
            raise ValueError("No weather data returned")

        print(hourly)
        weather_code = simple_weather_label(hourly["weathercode"][0])
        temp = hourly["temperature_2m"][0]
        precipitation = hourly["precipitation"][0]
        return f"Weather in {city_name} is {weather_code}. Temperature: {temp}C, Precipitation: {precipitation}."
    except Exception as e:
        print(e)
        return f"Weather in {city_name} is heavily cloudy."
    return f"Weather in {city_name} is heavily cloudy."


func_references = {"get_weather": get_weather}

registry = {
    f.name: convert_to_openai_function(f, strict=True) for f in func_references.values()
}
