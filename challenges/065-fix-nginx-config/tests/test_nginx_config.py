"""Tests for Challenge 065: Fix Nginx Config."""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

NGINX_PATH = Path(__file__).parent.parent / "setup" / "nginx.conf"


def read_config():
    return NGINX_PATH.read_text()


def test_ssl_redirect_exists():
    content = read_config()
    has_listen_80 = bool(re.search(r"listen\s+80", content))
    has_redirect = bool(re.search(r"return\s+301\s+https", content))
    assert has_listen_80, "Must have a server block listening on port 80"
    assert has_redirect, "Must redirect HTTP to HTTPS (return 301 https://...)"


def test_ssl_server_block():
    content = read_config()
    has_ssl_listen = bool(re.search(r"listen\s+443\s+ssl", content))
    assert has_ssl_listen, "Must have a server block listening on 443 with SSL"


def test_proxy_pass_correct_port():
    content = read_config()
    has_correct_proxy = bool(re.search(r"proxy_pass\s+http://localhost:8000", content))
    assert has_correct_proxy, "proxy_pass must point to http://localhost:8000"


def test_proxy_pass_trailing_slash():
    content = read_config()
    matches = re.findall(r"proxy_pass\s+(http://localhost:8000\S*)", content)
    assert len(matches) >= 1, "Must have proxy_pass to localhost:8000"
    for m in matches:
        clean = m.rstrip(";")
        assert clean.endswith("/"), \
            f"proxy_pass URL must end with trailing slash, got: {clean}"


def test_api_location_has_proxy_headers():
    content = read_config()
    api_section = ""
    in_api = False
    brace_count = 0
    for line in content.splitlines():
        if re.search(r"location\s+/api/", line):
            in_api = True
        if in_api:
            api_section += line + "\n"
            brace_count += line.count("{") - line.count("}")
            if brace_count <= 0 and in_api and "{" in api_section:
                break
    assert "X-Real-IP" in api_section, "API location must set X-Real-IP header"
    assert "X-Forwarded-For" in api_section, "API location must set X-Forwarded-For header"
    assert "Host" in api_section, "API location must set Host header"


def test_gzip_enabled():
    content = read_config()
    has_gzip_on = bool(re.search(r"gzip\s+on\s*;", content))
    assert has_gzip_on, "Gzip must be enabled (gzip on;)"


def test_gzip_types():
    content = read_config()
    has_gzip_types = bool(re.search(r"gzip_types\s+", content))
    assert has_gzip_types, "Must specify gzip_types"


def test_static_root():
    content = read_config()
    has_root = bool(re.search(r"root\s+/var/www/html\s*;", content))
    assert has_root, "Must serve static files from /var/www/html"
