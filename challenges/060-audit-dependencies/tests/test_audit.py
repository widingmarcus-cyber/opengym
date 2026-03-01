"""Tests for Challenge 060: Audit Dependencies."""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from audit import find_conflicts, find_vulnerable, find_unpinned

SETUP_DIR = str(Path(__file__).parent.parent / "setup")
REQ_PATH = os.path.join(SETUP_DIR, "requirements.txt")
SETUP_PATH = os.path.join(SETUP_DIR, "setup.cfg")
VULN_PATH = os.path.join(SETUP_DIR, "known_vulnerabilities.json")


def test_find_conflicts_count():
    conflicts = find_conflicts(REQ_PATH, SETUP_PATH)
    assert len(conflicts) == 5


def test_find_conflicts_packages():
    conflicts = find_conflicts(REQ_PATH, SETUP_PATH)
    names = [c["package"] for c in conflicts]
    assert names == ["click", "cryptography", "flask", "pydantic", "sqlalchemy"]


def test_find_conflicts_flask_versions():
    conflicts = find_conflicts(REQ_PATH, SETUP_PATH)
    flask_conflict = [c for c in conflicts if c["package"] == "flask"][0]
    assert flask_conflict["requirements_spec"] == "==2.3.2"
    assert flask_conflict["setup_spec"] == "==2.3.3"


def test_find_vulnerable_count():
    vulns = find_vulnerable(REQ_PATH, VULN_PATH)
    assert len(vulns) == 5


def test_find_vulnerable_packages():
    vulns = find_vulnerable(REQ_PATH, VULN_PATH)
    names = [v["package"] for v in vulns]
    assert names == ["cryptography", "gunicorn", "pillow", "requests", "sqlalchemy"]


def test_find_vulnerable_includes_cve():
    vulns = find_vulnerable(REQ_PATH, VULN_PATH)
    requests_vuln = [v for v in vulns if v["package"] == "requests"][0]
    assert requests_vuln["cve"] == "CVE-2023-32681"
    assert requests_vuln["version"] == "2.28.0"


def test_find_unpinned_count():
    unpinned = find_unpinned(REQ_PATH)
    assert len(unpinned) == 3


def test_find_unpinned_packages():
    unpinned = find_unpinned(REQ_PATH)
    assert unpinned == ["black", "isort", "python-dotenv"]
