"""Application configuration."""

import os


DATABASE_ENGINE = "postgresql"
DATABASE_HOST = os.environ.get("DB_HOST", "localhost")
DATABASE_PORT = int(os.environ.get("DB_PORT", "5432"))
DATABASE_NAME = "webapp_db"
SECRET_KEY = "dev-secret-key-change-in-production"
DEBUG = True
MAX_CONNECTIONS = 10

# TODO: add production configuration class
