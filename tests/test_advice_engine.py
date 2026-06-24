import pytest
from unittest.mock import patch, MagicMock
from anthropic import APIError
from src.advice_engine import generate_advice


SAMPLE_WEATHER = {
    "temperature_celsius": 22.5,
    "condition": "Clear",
    "description": "clear sky",
}

SAMPLE_EVENTS = [
    {"title": "Morning standup", "start": "2026-06-24T09:00:00", "end": "2026-06-24T09:30:00", "location": "Istanbul"},
    {"title": "Evening run", "start": "2026-06-24T18:00:00", "end": "2026-06-24T19:00:00", "location": "Istanbul"},
]


def _make_mock_message(text: str) -> MagicMock:
    """Build a mock Anthropic Message object with a single text content block."""
    content_block = MagicMock()
    content_block.text = text
    message = MagicMock()
    message.content = [content_block]
    return message


@patch("src.advice_engine.Anthropic")
@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
def test_generate_advice_success(mock_anthropic_class: MagicMock) -> None:
    expected_text = "Great weather for your standup. Perfect conditions for an evening run!"
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _make_mock_message(expected_text)
    mock_anthropic_class.return_value = mock_client

    result = generate_advice(SAMPLE_EVENTS, SAMPLE_WEATHER)

    assert result == expected_text
    mock_client.messages.create.assert_called_once()
    call_kwargs = mock_client.messages.create.call_args.kwargs
    assert call_kwargs["model"] == "claude-opus-4-8"
    assert call_kwargs["messages"][0]["role"] == "user"


@patch("src.advice_engine.Anthropic")
@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
def test_generate_advice_prompt_contains_weather_and_events(mock_anthropic_class: MagicMock) -> None:
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _make_mock_message("Some advice.")
    mock_anthropic_class.return_value = mock_client

    generate_advice(SAMPLE_EVENTS, SAMPLE_WEATHER)

    prompt = mock_client.messages.create.call_args.kwargs["messages"][0]["content"]
    assert "22.5" in prompt
    assert "clear sky" in prompt
    assert "Morning standup" in prompt
    assert "Evening run" in prompt


@patch.dict("os.environ", {}, clear=True)
def test_generate_advice_missing_api_key() -> None:
    with patch("src.advice_engine.os.getenv", return_value=None):
        with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY is not set"):
            generate_advice(SAMPLE_EVENTS, SAMPLE_WEATHER)


@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
def test_generate_advice_no_events() -> None:
    result = generate_advice([], SAMPLE_WEATHER)
    assert "No events" in result


@patch("src.advice_engine.Anthropic")
@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
def test_generate_advice_api_error(mock_anthropic_class: MagicMock) -> None:
    mock_client = MagicMock()
    mock_client.messages.create.side_effect = APIError(
        message="service unavailable", request=MagicMock(), body={}
    )
    mock_anthropic_class.return_value = mock_client

    with pytest.raises(RuntimeError, match="Claude API error"):
        generate_advice(SAMPLE_EVENTS, SAMPLE_WEATHER)
