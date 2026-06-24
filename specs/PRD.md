# PRD.md — Weather-Aware Personal Assistant

## 1. Problem / Purpose
A CLI personal assistant that combines the user's daily schedule (`calendar.json`) with current/upcoming weather data to generate practical, personalized advice.

**Why?** People typically check their calendar, then separately check the weather, and mentally combine the two ("my meeting is outdoors, it's raining, I should bring an umbrella"). This assistant automates that combination and delivers the advice directly.

## 2. User
An individual user (student/professional) with a daily schedule that includes outdoor or location-based events.

## 3. Core Features (Goals)
1. **Fetch weather data** — Pull current/daily weather data from the OpenWeather API for a user-specified location.
2. **Read schedule** — Read today's (or upcoming) events from `calendar.json`.
3. **Generate advice** — Combine weather and calendar data and generate natural-language, practical advice via the **Claude API** (LLM-powered).
4. **CLI interface** — User runs a command in the terminal and sees output in a readable format.

## 4. Inputs
- `calendar.json` — list of events, each with `title`, `start`, `end`, `location`.
- Location info (city name or coordinates) — via CLI argument or config.
- OpenWeather API key (stored in `.env`, never hardcoded).
- Anthropic API key (for Claude, stored in `.env`).

## 5. Output / Success State
When the user runs the command in the terminal, they see:
- A summary of the day's weather.
- A list of today's event(s).
- Weather-informed advice for each event (or overall), in natural language (e.g., "For your 2 PM meeting...").
- On error (API down, malformed `calendar.json`, etc.), a meaningful error message — no crashes.

## 6. Out of Scope
- Real calendar integration (Google Calendar, etc.) — local JSON file only.
- Graphical interface (GUI) — CLI only.
- Historical weather analysis or forecast-accuracy testing.

## 7. Advice Logic — Decision (LLM-Powered)
Not rule-based. Will use the **Claude API**: weather data and calendar events are sent to Claude within a prompt, and Claude generates context-aware advice in natural language. This choice gives more flexible, generalizable advice than fixed if/else rules (e.g., the "rain + outdoor event" combination is interpreted by Claude's own contextual understanding, rather than us hardcoding every scenario).

## 8. Success Metrics
- App runs without crashing.
- Produces sensible advice across at least 3 different weather scenarios (sunny, rainy, cold).
- Tests pass (in the `tests/` folder).
