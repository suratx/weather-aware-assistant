import pytest
from unittest.mock import patch, MagicMock
from src.cli import run

WEATHER = {"temperature_celsius": 18.0, "condition": "Rain", "description": "light rain"}
EVENTS = [
    {"title": "Team standup", "start": "2026-06-24T09:00:00", "end": "2026-06-24T09:30:00", "location": "Istanbul"},
]


@patch("src.cli.generate_advice", return_value="Bring an umbrella to your standup.")
@patch("src.cli.get_todays_events", return_value=EVENTS)
@patch("src.cli.get_weather", return_value=WEATHER)
@patch("builtins.input", return_value="Istanbul")
def test_run_happy_path(mock_input, mock_weather, mock_events, mock_advice, capsys) -> None:
    run()
    out = capsys.readouterr().out
    assert "Rain" in out
    assert "light rain" in out
    assert "18.0" in out
    assert "Team standup" in out
    assert "Bring an umbrella" in out


@patch("src.cli.get_todays_events", return_value=[])
@patch("src.cli.get_weather", return_value=WEATHER)
@patch("builtins.input", return_value="Istanbul")
def test_run_no_events_skips_advice(mock_input, mock_weather, mock_events, capsys) -> None:
    with patch("src.cli.generate_advice") as mock_advice:
        run()
        mock_advice.assert_not_called()
    out = capsys.readouterr().out
    assert "No events scheduled" in out


@patch("builtins.input", return_value="")
def test_run_empty_location(mock_input, capsys) -> None:
    run()
    out = capsys.readouterr().out
    assert "Error" in out
    assert "empty" in out


@patch("src.cli.get_weather", side_effect=RuntimeError("city not found"))
@patch("builtins.input", return_value="Nowhere")
def test_run_weather_error(mock_input, mock_weather, capsys) -> None:
    run()
    out = capsys.readouterr().out
    assert "Error fetching weather" in out
    assert "city not found" in out


@patch("src.cli.get_todays_events", side_effect=RuntimeError("calendar.json not found"))
@patch("src.cli.get_weather", return_value=WEATHER)
@patch("builtins.input", return_value="Istanbul")
def test_run_calendar_error(mock_input, mock_weather, mock_events, capsys) -> None:
    run()
    out = capsys.readouterr().out
    assert "Error reading calendar" in out
    assert "calendar.json not found" in out


@patch("src.cli.generate_advice", side_effect=RuntimeError("API key missing"))
@patch("src.cli.get_todays_events", return_value=EVENTS)
@patch("src.cli.get_weather", return_value=WEATHER)
@patch("builtins.input", return_value="Istanbul")
def test_run_advice_error(mock_input, mock_weather, mock_events, mock_advice, capsys) -> None:
    run()
    out = capsys.readouterr().out
    assert "Error generating advice" in out
    assert "API key missing" in out
