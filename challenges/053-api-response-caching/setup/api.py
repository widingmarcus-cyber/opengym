class FakeAPI:
    """Simulated API with call counting."""

    def __init__(self, data=None):
        self._data = data or {}
        self.call_count = 0

    def get(self, key):
        """Fetch data for the given key."""
        self.call_count += 1
        if key in self._data:
            return self._data[key]
        raise KeyError(f"No data for key: {key}")
