import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(location: str) -> dict:
    """Fetch current weather for a location from the OpenWeather API.

    Returns a dict with keys: temperature_celsius, condition, description.
    Raises RuntimeError on API or network failure.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY is not set in the environment.")

    params = {"q": location, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Weather API error ({response.status_code}): {response.text}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error while fetching weather: {e}") from e

    data = response.json()

    return {
        "temperature_celsius": data["main"]["temp"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
    }
