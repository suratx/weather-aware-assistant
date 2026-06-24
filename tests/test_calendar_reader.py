import json
import pytest
from datetime import date
from pathlib import Path
from src.calendar_reader import get_todays_events

TODAY = date(2026, 6, 24)
TOMORROW = date(2026, 6, 25)


def write_calendar(tmp_path: Path, events: list) -> Path:
    """Write a list of events to a temporary calendar.json and return its path."""
    p = tmp_path / "calendar.json"
    p.write_text(json.dumps(events), encoding="utf-8")
    return p


SAMPLE_EVENTS = [
    {"title": "Morning standup", "start": "2026-06-24T09:00:00", "end": "2026-06-24T09:30:00", "location": "Istanbul"},
    {"title": "Lunch with client", "start": "2026-06-24T12:30:00", "end": "2026-06-24T13:30:00", "location": "Istanbul"},
    {"title": "Team offsite", "start": "2026-06-25T10:00:00", "end": "2026-06-25T12:00:00", "location": "Ankara"},
]


def test_returns_only_todays_events(tmp_path: Path) -> None:
    path = write_calendar(tmp_path, SAMPLE_EVENTS)
    result = get_todays_events(calendar_path=path, today=TODAY)
    assert len(result) == 2
    assert all(e["start"].startswith("2026-06-24") for e in result)


def test_returns_empty_when_no_events_today(tmp_path: Path) -> None:
    path = write_calendar(tmp_path, SAMPLE_EVENTS)
    result = get_todays_events(calendar_path=path, today=TOMORROW)
    assert len(result) == 1
    assert result[0]["title"] == "Team offsite"


def test_returns_empty_list_for_empty_calendar(tmp_path: Path) -> None:
    path = write_calendar(tmp_path, [])
    result = get_todays_events(calendar_path=path, today=TODAY)
    assert result == []


def test_raises_on_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "nonexistent.json"
    with pytest.raises(RuntimeError, match="Calendar file not found"):
        get_todays_events(calendar_path=missing, today=TODAY)


def test_raises_on_invalid_json(tmp_path: Path) -> None:
    p = tmp_path / "calendar.json"
    p.write_text("not valid json", encoding="utf-8")
    with pytest.raises(RuntimeError, match="not valid JSON"):
        get_todays_events(calendar_path=p, today=TODAY)


def test_raises_when_root_is_not_list(tmp_path: Path) -> None:
    p = write_calendar(tmp_path, {"key": "value"})  # type: ignore[arg-type]
    with pytest.raises(RuntimeError, match="must contain a JSON array"):
        get_todays_events(calendar_path=p, today=TODAY)


def test_raises_on_event_missing_required_field(tmp_path: Path) -> None:
    bad_event = {"title": "No location", "start": "2026-06-24T09:00:00", "end": "2026-06-24T10:00:00"}
    path = write_calendar(tmp_path, [bad_event])
    with pytest.raises(RuntimeError, match="missing required fields"):
        get_todays_events(calendar_path=path, today=TODAY)


def test_raises_on_invalid_start_date(tmp_path: Path) -> None:
    bad_event = {"title": "Bad date", "start": "not-a-date", "end": "2026-06-24T10:00:00", "location": "Istanbul"}
    path = write_calendar(tmp_path, [bad_event])
    with pytest.raises(RuntimeError, match="invalid start date"):
        get_todays_events(calendar_path=path, today=TODAY)
