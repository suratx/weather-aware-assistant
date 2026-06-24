import os
from anthropic import Anthropic, APIError
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-opus-4-8"


def _build_prompt(events: list, weather: dict) -> str:
    """Construct the user prompt combining weather data and today's events."""
    event_lines = "\n".join(
        f"- {e['title']} from {e['start'][11:16]} to {e['end'][11:16]} in {e['location']}"
        for e in events
    )
    return (
        f"Today's weather: {weather['condition']} ({weather['description']}), "
        f"{weather['temperature_celsius']:.1f}°C.\n\n"
        f"Today's events:\n{event_lines}\n\n"
        "For each event, give brief, practical, weather-aware advice in a friendly tone. "
        "Be concise — one or two sentences per event."
    )


def generate_advice(events: list, weather: dict) -> str:
    """Call the Claude API to generate weather-informed advice for today's events.

    Raises RuntimeError if the API key is missing or the API call fails.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set in the environment.")

    if not events:
        return "No events scheduled for today — enjoy your free day!"

    client = Anthropic(api_key=api_key)
    prompt = _build_prompt(events, weather)

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
    except APIError as e:
        raise RuntimeError(f"Claude API error: {e}") from e

    return message.content[0].text
