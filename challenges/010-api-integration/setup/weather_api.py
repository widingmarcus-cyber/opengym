"""Simulated Weather API — DO NOT MODIFY THIS FILE."""


_WEATHER_DATA = {
    "london": {"city": "London", "temperature": 12, "condition": "cloudy", "humidity": 75, "wind_speed": 15},
    "paris": {"city": "Paris", "temperature": 18, "condition": "sunny", "humidity": 55, "wind_speed": 10},
    "tokyo": {"city": "Tokyo", "temperature": 22, "condition": "rainy", "humidity": 80, "wind_speed": 20},
    "new york": {"city": "New York", "temperature": 8, "condition": "cloudy", "humidity": 65, "wind_speed": 25},
    "sydney": {"city": "Sydney", "temperature": 28, "condition": "sunny", "humidity": 45, "wind_speed": 12},
    "berlin": {"city": "Berlin", "temperature": 5, "condition": "snowy", "humidity": 85, "wind_speed": 30},
    "mumbai": {"city": "Mumbai", "temperature": 33, "condition": "sunny", "humidity": 70, "wind_speed": 8},
    "cairo": {"city": "Cairo", "temperature": 35, "condition": "sunny", "humidity": 20, "wind_speed": 5},
}

_FORECAST_PATTERNS = {
    "london": [
        {"temperature": 13, "condition": "rainy", "humidity": 80},
        {"temperature": 11, "condition": "cloudy", "humidity": 70},
        {"temperature": 14, "condition": "sunny", "humidity": 60},
        {"temperature": 10, "condition": "rainy", "humidity": 85},
        {"temperature": 12, "condition": "cloudy", "humidity": 75},
        {"temperature": 15, "condition": "sunny", "humidity": 55},
        {"temperature": 9, "condition": "rainy", "humidity": 90},
    ],
    "paris": [
        {"temperature": 19, "condition": "sunny", "humidity": 50},
        {"temperature": 17, "condition": "cloudy", "humidity": 60},
        {"temperature": 20, "condition": "sunny", "humidity": 45},
        {"temperature": 16, "condition": "rainy", "humidity": 70},
        {"temperature": 18, "condition": "sunny", "humidity": 55},
        {"temperature": 21, "condition": "sunny", "humidity": 40},
        {"temperature": 15, "condition": "cloudy", "humidity": 65},
    ],
    "tokyo": [
        {"temperature": 23, "condition": "rainy", "humidity": 85},
        {"temperature": 21, "condition": "rainy", "humidity": 82},
        {"temperature": 24, "condition": "cloudy", "humidity": 75},
        {"temperature": 20, "condition": "sunny", "humidity": 65},
        {"temperature": 22, "condition": "rainy", "humidity": 80},
        {"temperature": 25, "condition": "sunny", "humidity": 60},
        {"temperature": 19, "condition": "cloudy", "humidity": 70},
    ],
    "new york": [
        {"temperature": 9, "condition": "sunny", "humidity": 55},
        {"temperature": 7, "condition": "cloudy", "humidity": 70},
        {"temperature": 10, "condition": "sunny", "humidity": 50},
        {"temperature": 6, "condition": "snowy", "humidity": 80},
        {"temperature": 8, "condition": "cloudy", "humidity": 65},
        {"temperature": 11, "condition": "sunny", "humidity": 45},
        {"temperature": 5, "condition": "snowy", "humidity": 85},
    ],
    "sydney": [
        {"temperature": 27, "condition": "sunny", "humidity": 50},
        {"temperature": 29, "condition": "sunny", "humidity": 40},
        {"temperature": 26, "condition": "cloudy", "humidity": 55},
        {"temperature": 30, "condition": "sunny", "humidity": 35},
        {"temperature": 25, "condition": "rainy", "humidity": 70},
        {"temperature": 28, "condition": "sunny", "humidity": 45},
        {"temperature": 31, "condition": "sunny", "humidity": 30},
    ],
    "berlin": [
        {"temperature": 3, "condition": "snowy", "humidity": 90},
        {"temperature": 6, "condition": "cloudy", "humidity": 80},
        {"temperature": 4, "condition": "snowy", "humidity": 85},
        {"temperature": 7, "condition": "cloudy", "humidity": 75},
        {"temperature": 2, "condition": "snowy", "humidity": 92},
        {"temperature": 8, "condition": "sunny", "humidity": 65},
        {"temperature": 1, "condition": "snowy", "humidity": 95},
    ],
    "mumbai": [
        {"temperature": 34, "condition": "sunny", "humidity": 65},
        {"temperature": 32, "condition": "cloudy", "humidity": 75},
        {"temperature": 35, "condition": "sunny", "humidity": 60},
        {"temperature": 31, "condition": "rainy", "humidity": 85},
        {"temperature": 33, "condition": "sunny", "humidity": 70},
        {"temperature": 36, "condition": "sunny", "humidity": 55},
        {"temperature": 30, "condition": "rainy", "humidity": 90},
    ],
    "cairo": [
        {"temperature": 36, "condition": "sunny", "humidity": 18},
        {"temperature": 34, "condition": "sunny", "humidity": 22},
        {"temperature": 37, "condition": "sunny", "humidity": 15},
        {"temperature": 33, "condition": "sunny", "humidity": 25},
        {"temperature": 35, "condition": "sunny", "humidity": 20},
        {"temperature": 38, "condition": "sunny", "humidity": 12},
        {"temperature": 32, "condition": "sunny", "humidity": 28},
    ],
}


class WeatherAPI:
    """Simulated weather API client."""

    def current(self, city: str) -> dict:
        """Get current weather for a city."""
        key = city.lower().strip()
        if key not in _WEATHER_DATA:
            raise ValueError(f"City not found: {city}")
        return dict(_WEATHER_DATA[key])

    def forecast(self, city: str, days: int = 3) -> list:
        """Get forecast for the next N days."""
        key = city.lower().strip()
        if key not in _FORECAST_PATTERNS:
            raise ValueError(f"City not found: {city}")
        if days < 1 or days > 7:
            raise ValueError(f"Days must be between 1 and 7, got {days}")
        pattern = _FORECAST_PATTERNS[key]
        return [{"day": i + 1, **pattern[i]} for i in range(days)]
