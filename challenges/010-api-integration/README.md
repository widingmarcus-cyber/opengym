# Challenge 010: API Client Integration

## Difficulty: Hard

## Task

Write an API client in `setup/weather_client.py` that interacts with a weather service. The API is simulated by a local module — no internet required.

Read the API documentation in `setup/weather_api_docs.md`, then implement the client functions.

## Functions to Implement

1. `get_current_weather(city)` — Returns current weather dict for a city, or `None` if city not found
2. `get_forecast(city, days=3)` — Returns a list of forecast dicts for the next N days (max 7)
3. `get_coldest_city(cities)` — Given a list of city names, returns the name of the city with the lowest current temperature
4. `will_it_rain(city, days=3)` — Returns `True` if any day in the forecast has condition "rainy"
5. `format_report(city)` — Returns a formatted multi-line string report for a city

## Rules

- Only modify `setup/weather_client.py`
- Use the provided `setup/weather_api.py` module (do NOT modify it)
- Read `setup/weather_api_docs.md` for the API specification
- Handle errors gracefully (invalid cities, API errors)
