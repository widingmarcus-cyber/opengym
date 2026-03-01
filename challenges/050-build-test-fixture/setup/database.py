"""In-memory database for testing."""

from typing import Any, Dict, List, Optional


class InMemoryDB:
    """A simple in-memory database that stores objects by collection and id."""

    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def insert(self, collection: str, obj: Any) -> None:
        """Insert an object into a collection. Object must have an 'id' attribute."""
        if collection not in self._store:
            self._store[collection] = {}
        self._store[collection][obj.id] = obj

    def get(self, collection: str, obj_id: str) -> Optional[Any]:
        """Get an object by id from a collection. Returns None if not found."""
        return self._store.get(collection, {}).get(obj_id)

    def query(self, collection: str, **filters) -> List[Any]:
        """Query objects in a collection matching all given attribute filters."""
        if collection not in self._store:
            return []
        results = []
        for obj in self._store[collection].values():
            match = True
            for attr, value in filters.items():
                if not hasattr(obj, attr) or getattr(obj, attr) != value:
                    match = False
                    break
            if match:
                results.append(obj)
        return results

    def delete(self, collection: str, obj_id: str) -> bool:
        """Delete an object by id. Returns True if deleted, False if not found."""
        if collection in self._store and obj_id in self._store[collection]:
            del self._store[collection][obj_id]
            return True
        return False

    def count(self, collection: str) -> int:
        """Return the number of objects in a collection."""
        return len(self._store.get(collection, {}))
