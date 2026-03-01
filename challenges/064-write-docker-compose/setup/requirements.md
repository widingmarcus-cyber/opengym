# Docker Compose Requirements

## Services

### 1. Web Application (`web`)
- **Image**: `python:3.11-slim`
- **Container name**: `webapp`
- **Ports**: Map host port `8080` to container port `5000`
- **Environment variables**:
  - `DATABASE_URL=postgresql://appuser:secret@db:5432/appdb`
  - `REDIS_URL=redis://cache:6379/0`
  - `FLASK_ENV=production`
- **Volumes**: Mount `./app` to `/app` in the container
- **Depends on**: `db` and `cache` services
- **Command**: `python app.py`

### 2. PostgreSQL Database (`db`)
- **Image**: `postgres:15`
- **Container name**: `postgres_db`
- **Environment variables**:
  - `POSTGRES_USER=appuser`
  - `POSTGRES_PASSWORD=secret`
  - `POSTGRES_DB=appdb`
- **Volumes**: Use a named volume `pgdata` mounted to `/var/lib/postgresql/data`
- **Ports**: Map host port `5432` to container port `5432`

### 3. Redis Cache (`cache`)
- **Image**: `redis:7-alpine`
- **Container name**: `redis_cache`
- **Ports**: Map host port `6379` to container port `6379`
- **Command**: `redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru`

## Volumes

Declare a named volume `pgdata` at the top level.

## Network

All services should be on the default network (no custom network configuration needed).
