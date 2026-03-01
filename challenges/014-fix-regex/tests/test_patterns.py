"""Tests for Challenge 014: Fix the Broken Regexes."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from patterns import validate_email, validate_phone, validate_url, validate_date, validate_ipv4


# --- Email ---

def test_email_valid():
    assert validate_email("user@example.com") is True
    assert validate_email("alice.bob@domain.org") is True
    assert validate_email("test_user@mail.co.uk") is True


def test_email_invalid():
    assert validate_email("not-an-email") is False
    assert validate_email("user@example.com EXTRA") is False
    assert validate_email("@example.com") is False
    assert validate_email("user@") is False


# --- Phone ---

def test_phone_valid():
    assert validate_phone("(555) 123-4567") is True
    assert validate_phone("(800) 000-0000") is True


def test_phone_invalid():
    assert validate_phone("555-123-4567") is False
    assert validate_phone("(555) 123-4567 ext 9") is False
    assert validate_phone("(55) 123-4567") is False


# --- URL ---

def test_url_valid():
    assert validate_url("http://example.com") is True
    assert validate_url("https://example.com") is True
    assert validate_url("https://example.com/path/to/page") is True


def test_url_invalid():
    assert validate_url("ftp://example.com") is False
    assert validate_url("example.com") is False
    assert validate_url("https://") is False


# --- Date ---

def test_date_valid():
    assert validate_date("2024-01-15") is True
    assert validate_date("1999-12-31") is True
    assert validate_date("2000-06-01") is True


def test_date_invalid():
    assert validate_date("2024-13-01") is False
    assert validate_date("2024-00-15") is False
    assert validate_date("2024-01-32") is False
    assert validate_date("24-01-15") is False


# --- IPv4 ---

def test_ipv4_valid():
    assert validate_ipv4("192.168.1.1") is True
    assert validate_ipv4("0.0.0.0") is True
    assert validate_ipv4("255.255.255.255") is True


def test_ipv4_invalid():
    assert validate_ipv4("256.1.1.1") is False
    assert validate_ipv4("192.168.1") is False
    assert validate_ipv4("01.01.01.01") is False
    assert validate_ipv4("192.168.1.1.1") is False


# --- Additional boundary / rejection tests ---

def test_email_trailing_garbage():
    """Email with trailing non-email characters must be rejected."""
    assert validate_email("user@example.com!!!") is False


def test_date_slashes_invalid():
    """Date with slashes instead of dashes must be rejected."""
    assert validate_date("2024/01/15") is False


def test_url_no_protocol():
    """URL without http:// or https:// must be rejected."""
    assert validate_url("example.com/path") is False


def test_phone_with_letters():
    """Phone number containing letters must be rejected."""
    assert validate_phone("(555) abc-defg") is False


def test_ipv4_octet_above_255():
    """IPv4 with octets above 255 must be rejected."""
    assert validate_ipv4("999.999.999.999") is False


# --- More tests targeting specific regex bugs ---

def test_email_trailing_space():
    """Email with trailing whitespace must be rejected (match vs fullmatch bug)."""
    assert validate_email("user@example.com ") is False


def test_email_trailing_newline():
    assert validate_email("user@example.com\ninjected") is False


def test_phone_trailing_text():
    """Phone with extra trailing text must be rejected."""
    assert validate_phone("(123) 456-7890 x5") is False


def test_url_https_basic():
    """https URLs must be accepted (url pattern only matches http bug)."""
    assert validate_url("https://google.com") is True


def test_url_https_with_path():
    assert validate_url("https://example.com/some/path") is True


def test_date_dash_format():
    """Dates with dashes must be accepted (pattern uses / instead of - bug)."""
    assert validate_date("2000-01-01") is True


def test_date_another_dash():
    assert validate_date("1985-06-15") is True


def test_ipv4_leading_zeros_single():
    """Leading zeros must be rejected."""
    assert validate_ipv4("192.168.01.1") is False
