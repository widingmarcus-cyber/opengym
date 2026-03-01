"""Database connection layer."""

import sqlite3
from config import DATABASE_ENGINE, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME


class DatabaseConnection:
    """Manages database connections."""

    def __init__(self, engine, host, port, name):
        self.engine = engine
        self.host = host
        self.port = port
        self.name = name
        self._connection = None

    def connect(self):
        """Establish a database connection."""
        self._connection = True
        return self

    def disconnect(self):
        """Close the database connection."""
        self._connection = None

    def is_connected(self):
        """Check if connected."""
        return self._connection is not None

    def execute_query(self, query, params=None):
        """Execute a database query."""
        if not self.is_connected():
            raise RuntimeError("Not connected to database")
        return []


# TODO: add connection pooling support

def get_db():
    """Get the default database connection."""
    return DatabaseConnection(DATABASE_ENGINE, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)
