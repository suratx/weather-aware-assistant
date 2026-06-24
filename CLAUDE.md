# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A CLI personal assistant that reads today's events from `calendar.json`, fetches weather from the OpenWeather API, and uses the Claude API to generate natural-language, weather-informed advice for each event.

## Tech Stack

- Python 3.11+
- OpenWeather API for weather data
- Anthropic Claude API (`claude-sonnet` model) for advice generation
- pytest for testing
- `python-dotenv` for environment variable management
- `requirements.txt` for dependencies (plain venv, no Poetry/Pipenv)

## Commands

```bash
# Set up environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run the assistant
python src/main.py --location "Istanbul"

# Run all tests
pytest tests/

# Run a single test file
pytest tests/test_weather_client.py
```

## Architecture

The app is split into four single-responsibility modules under `src/`:

| File | Responsibility |
|---|---|
| `src/weather_client.py` | OpenWeather API calls only |
| `src/calendar_reader.py` | Read/parse `calendar.json` |
| `src/advice_engine.py` | Build Claude prompt and call Anthropic API |
| `src/cli.py` | CLI entry point; orchestrates the three modules above |
| `src/main.py` | Thin entry point that calls `cli.py` |

**Data flow:** `cli.py` calls `weather_client` and `calendar_reader` in parallel, passes both results to `advice_engine`, and prints the output.

**`calendar.json` schema:** each event has `title`, `start`, `end`, `location`.

**Environment variables** (in `.env`, never committed):
- `OPENWEATHER_API_KEY`
- `ANTHROPIC_API_KEY`

## Constraints

- Do not add features beyond what is in `specs/PRD.md`.
- Do not modify files outside the one(s) being worked on in the current step.
- Every new piece of logic must have a corresponding test in `tests/`.
- No unhandled exceptions — all errors must print a clear user-facing message and exit cleanly.
- Validate all external input (API responses, `calendar.json` contents) before use.

## Code Style

- PEP8, type hints on all function signatures, one short docstring per function.
- Prefer readability over cleverness — this codebase should be easy for a beginner to follow.
- Do not mix API logic, file I/O, and CLI/print statements in the same file.
