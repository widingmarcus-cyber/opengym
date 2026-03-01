# Weather API Documentation

## Overview

This is a simulated weather API. Import and use it like a regular Python module.

## Usage

```python
from weather_api import WeatherAPI

api = WeatherAPI()
```

## Methods

### `api.current(city: str) -> dict`

Returns current weather for a city.

**Parameters:**
- `city` (str): City name (case-insensitive)

**Returns:**
```python
{
    "city": "London",
    "temperature": 12,      # Celsius
    "condition": "cloudy",   # "sunny", "cloudy", "rainy", "snowy"
    "humidity": 75,          # Percentage
    "wind_speed": 15         # km/h
}
```

**Raises:**
- `ValueError` if city is not found in the database

### `api.forecast(city: str, days: int) -> list[dict]`

Returns forecast for the next N days.

**Parameters:**
- `city` (str): City name (case-insensitive)
- `days` (int): Number of days (1-7, default 3)

**Returns:** List of dicts, each with:
```python
{
    "day": 1,
    "temperature": 14,
    "condition": "sunny",
    "humidity": 60
}
```

**Raises:**
- `ValueError` if city not found
- `ValueError` if days < 1 or days > 7

### Available Cities

London, Paris, Tokyo, New York, Sydney, Berlin, Mumbai, Cairo
