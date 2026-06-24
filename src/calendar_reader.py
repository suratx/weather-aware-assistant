import json
from datetime import date
from pathlib import Path
from typing import Optional

CALENDAR_PATH = Path(__file__).parent.parent / "calendar.json"

REQUIRED_FIELDS = {"title", "start", "end", "location"}


def _validate_event(event: dict) -> bool:
    """Return True if an event dict contains all required string fields."""
    if not isinstance(event, dict):
        return False
    return all(field in event and isinstance(event[field], str) for field in REQUIRED_FIELDS)


def get_todays_events(
    calendar_path: Path = CALENDAR_PATH,
    today: Optional[date] = None,
) -> list[dict]:
    """Read calendar.json and return events whose start date matches today.

    Raises RuntimeError if the file is missing or its contents are malformed.
    """
    if today is None:
        today = date.today()

    if not calendar_path.exists():
        raise RuntimeError(f"Calendar file not found: {calendar_path}")

    try:
        with open(calendar_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"calendar.json is not valid JSON: {e}") from e

    if not isinstance(data, list):
        raise RuntimeError("calendar.json must contain a JSON array of events.")

    today_events = []
    for i, event in enumerate(data):
        if not _validate_event(event):
            raise RuntimeError(
                f"Event at index {i} is missing required fields or has invalid types. "
                f"Required: {sorted(REQUIRED_FIELDS)}"
            )
        try:
            event_date = date.fromisoformat(event["start"][:10])
        except ValueError as e:
            raise RuntimeError(
                f"Event '{event.get('title', f'index {i}')}' has an invalid start date: {e}"
            ) from e

        if event_date == today:
            today_events.append(event)

    return today_events
