import pytest
from unittest.mock import patch, MagicMock
from src.weather_client import get_weather
import requests


MOCK_API_RESPONSE = {
    "main": {"temp": 22.5},
    "weather": [{"main": "Clear", "description": "clear sky"}],
}


@patch("src.weather_client.requests.get")
@patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test-key"})
def test_get_weather_success(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = MOCK_API_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_weather("London")

    assert result == {
        "temperature_celsius": 22.5,
        "condition": "Clear",
        "description": "clear sky",
    }
    mock_get.assert_called_once()
    call_kwargs = mock_get.call_args
    assert call_kwargs.kwargs["params"]["q"] == "London"
    assert call_kwargs.kwargs["params"]["units"] == "metric"


@patch.dict("os.environ", {}, clear=True)
def test_get_weather_missing_api_key() -> None:
    with patch("src.weather_client.os.getenv", return_value=None):
        with pytest.raises(RuntimeError, match="OPENWEATHER_API_KEY is not set"):
            get_weather("London")


@patch("src.weather_client.requests.get")
@patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test-key"})
def test_get_weather_http_error(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "city not found"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="Weather API error"):
        get_weather("NonexistentCity")


@patch("src.weather_client.requests.get")
@patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test-key"})
def test_get_weather_network_error(mock_get: MagicMock) -> None:
    mock_get.side_effect = requests.exceptions.ConnectionError("connection refused")

    with pytest.raises(RuntimeError, match="Network error while fetching weather"):
        get_weather("London")
