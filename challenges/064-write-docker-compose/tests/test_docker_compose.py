"""Tests for Challenge 064: Write Docker Compose."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import yaml

COMPOSE_PATH = Path(__file__).parent.parent / "setup" / "docker-compose.yml"


def load_compose():
    content = COMPOSE_PATH.read_text()
    return yaml.safe_load(content)


def test_valid_yaml():
    content = COMPOSE_PATH.read_text()
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise AssertionError(f"YAML is invalid: {e}")
    assert isinstance(data, dict), "Must be a valid YAML mapping"


def test_three_services_exist():
    data = load_compose()
    services = data.get("services", {})
    assert "web" in services, "Must have a 'web' service"
    assert "db" in services, "Must have a 'db' service"
    assert "cache" in services, "Must have a 'cache' service"


def test_web_service_config():
    data = load_compose()
    web = data["services"]["web"]
    assert "python" in web.get("image", "").lower(), "Web must use a Python image"
    assert web.get("container_name") == "webapp", "Web container_name must be 'webapp'"


def test_web_service_ports():
    data = load_compose()
    web = data["services"]["web"]
    ports = web.get("ports", [])
    port_strs = [str(p) for p in ports]
    matched = any("8080" in p and "5000" in p for p in port_strs)
    assert matched, "Web must map host port 8080 to container port 5000"


def test_web_service_env_vars():
    data = load_compose()
    web = data["services"]["web"]
    env = web.get("environment", [])
    if isinstance(env, list):
        env_str = " ".join(env)
    elif isinstance(env, dict):
        env_str = " ".join(f"{k}={v}" for k, v in env.items())
    else:
        env_str = ""
    assert "DATABASE_URL" in env_str, "Web must have DATABASE_URL"
    assert "REDIS_URL" in env_str, "Web must have REDIS_URL"
    assert "FLASK_ENV" in env_str, "Web must have FLASK_ENV"


def test_web_depends_on():
    data = load_compose()
    web = data["services"]["web"]
    depends = web.get("depends_on", [])
    if isinstance(depends, dict):
        depends = list(depends.keys())
    assert "db" in depends, "Web must depend on db"
    assert "cache" in depends, "Web must depend on cache"


def test_db_service_config():
    data = load_compose()
    db = data["services"]["db"]
    assert "postgres" in db.get("image", "").lower(), "DB must use a PostgreSQL image"
    env = db.get("environment", [])
    if isinstance(env, list):
        env_str = " ".join(env)
    elif isinstance(env, dict):
        env_str = " ".join(f"{k}={v}" for k, v in env.items())
    else:
        env_str = ""
    assert "POSTGRES_USER" in env_str, "DB must have POSTGRES_USER"
    assert "POSTGRES_PASSWORD" in env_str, "DB must have POSTGRES_PASSWORD"
    assert "POSTGRES_DB" in env_str, "DB must have POSTGRES_DB"


def test_db_volume():
    data = load_compose()
    db = data["services"]["db"]
    volumes = db.get("volumes", [])
    volume_strs = [str(v) for v in volumes]
    matched = any("pgdata" in v and "/var/lib/postgresql/data" in v for v in volume_strs)
    assert matched, "DB must mount pgdata to /var/lib/postgresql/data"


def test_cache_service_config():
    data = load_compose()
    cache = data["services"]["cache"]
    assert "redis" in cache.get("image", "").lower(), "Cache must use a Redis image"
    ports = cache.get("ports", [])
    port_strs = [str(p) for p in ports]
    matched = any("6379" in p for p in port_strs)
    assert matched, "Cache must expose port 6379"


def test_named_volume_declared():
    data = load_compose()
    volumes = data.get("volumes", {})
    assert volumes is not None, "Must declare top-level volumes"
    assert "pgdata" in volumes or (isinstance(volumes, dict) and "pgdata" in volumes), \
        "Must declare 'pgdata' named volume at top level"
