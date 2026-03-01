"""Tests for Challenge 087: Regex Crossword."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from patterns import (
    match_ipv4,
    match_iso_date,
    match_hex_color,
    match_semantic_version,
    match_quoted_string,
)


def test_ipv4_valid():
    pattern = match_ipv4()
    for addr in ["192.168.1.1", "0.0.0.0", "255.255.255.255", "10.0.0.1", "172.16.254.1"]:
        assert re.fullmatch(pattern, addr) is not None, f"Should match: {addr}"


def test_ipv4_invalid():
    pattern = match_ipv4()
    for addr in ["256.1.1.1", "192.168.1", "192.168.1.1.1", "01.01.01.01", "abc.def.ghi.jkl", "999.999.999.999"]:
        assert re.fullmatch(pattern, addr) is None, f"Should not match: {addr}"


def test_iso_date_valid():
    pattern = match_iso_date()
    for date in ["2024-01-15", "1999-12-31", "2000-06-01", "2024-02-28", "1970-01-01"]:
        assert re.fullmatch(pattern, date) is not None, f"Should match: {date}"


def test_iso_date_invalid():
    pattern = match_iso_date()
    for date in ["2024-13-01", "2024-00-15", "2024-01-32", "24-01-15", "2024-1-1", "2024/01/15"]:
        assert re.fullmatch(pattern, date) is None, f"Should not match: {date}"


def test_hex_color_valid():
    pattern = match_hex_color()
    for color in ["#fff", "#FF5733", "#000", "#abcdef", "#ABC", "#a1b2c3"]:
        assert re.fullmatch(pattern, color) is not None, f"Should match: {color}"


def test_hex_color_invalid():
    pattern = match_hex_color()
    for color in ["#ffff", "#GG0000", "fff", "#12345", "#", "##ffffff", "#abcdeg"]:
        assert re.fullmatch(pattern, color) is None, f"Should not match: {color}"


def test_semantic_version_valid():
    pattern = match_semantic_version()
    for ver in ["1.0.0", "0.1.0", "12.34.56", "1.0.0-alpha", "2.1.3-beta.1", "1.0.0-rc.2"]:
        assert re.fullmatch(pattern, ver) is not None, f"Should match: {ver}"


def test_semantic_version_invalid():
    pattern = match_semantic_version()
    for ver in ["1.0", "1.0.0.0", "v1.0.0", "1.0.0-", "1.0.0beta", ".1.0.0"]:
        assert re.fullmatch(pattern, ver) is None, f"Should not match: {ver}"


def test_quoted_string_valid():
    pattern = match_quoted_string()
    for s in ['"hello"', "'world'", '"say \\"hi\\""', "'don\\'t'", '""', "''"]:
        assert re.fullmatch(pattern, s) is not None, f"Should match: {s}"


def test_quoted_string_invalid():
    pattern = match_quoted_string()
    for s in ['"unclosed', "'mixed\"", "hello", "\"\"extra\""]:
        assert re.fullmatch(pattern, s) is None, f"Should not match: {s}"
