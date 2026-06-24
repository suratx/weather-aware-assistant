from src.weather_client import get_weather
from src.calendar_reader import get_todays_events
from src.advice_engine import generate_advice


def _print_weather(weather: dict) -> None:
    """Print a formatted weather summary."""
    print(f"\nWeather: {weather['condition']} — {weather['description']}, "
          f"{weather['temperature_celsius']:.1f}°C")


def _print_events(events: list) -> None:
    """Print today's events as a numbered list."""
    print(f"\nToday's events ({len(events)}):")
    for i, event in enumerate(events, start=1):
        start = event["start"][11:16]
        end = event["end"][11:16]
        print(f"  {i}. {event['title']} — {start}–{end} @ {event['location']}")


def run() -> None:
    """Orchestrate weather fetch, calendar read, and advice generation; print results."""
    location = input("Enter your location: ").strip()
    if not location:
        print("Error: location cannot be empty.")
        return

    print(f"\nFetching weather for {location}...")
    try:
        weather = get_weather(location)
    except RuntimeError as e:
        print(f"Error fetching weather: {e}")
        return

    try:
        events = get_todays_events()
    except RuntimeError as e:
        print(f"Error reading calendar: {e}")
        return

    _print_weather(weather)

    if not events:
        print("\nNo events scheduled for today.")
        return

    _print_events(events)

    print("\nGenerating advice...")
    try:
        advice = generate_advice(events, weather)
    except RuntimeError as e:
        print(f"Error generating advice: {e}")
        return

    print(f"\nAdvice:\n{advice}")
