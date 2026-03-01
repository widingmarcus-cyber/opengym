"""Tests for Challenge 085: Build Markdown Parser."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from md_parser import parse


def test_parse_single_heading():
    result = parse("# Hello World")
    assert len(result) == 1
    assert result[0] == {"type": "heading", "level": 1, "content": "Hello World"}


def test_parse_multiple_heading_levels():
    md = "# Title\n\n## Subtitle\n\n### Section"
    result = parse(md)
    assert len(result) == 3
    assert result[0]["level"] == 1
    assert result[1]["level"] == 2
    assert result[1]["content"] == "Subtitle"
    assert result[2]["level"] == 3


def test_parse_paragraph():
    md = "This is a simple paragraph."
    result = parse(md)
    assert len(result) == 1
    assert result[0] == {"type": "paragraph", "content": "This is a simple paragraph."}


def test_parse_code_block_with_language():
    md = '```python\ndef hello():\n    print("hi")\n```'
    result = parse(md)
    assert len(result) == 1
    assert result[0]["type"] == "code_block"
    assert result[0]["language"] == "python"
    assert 'def hello():' in result[0]["content"]
    assert 'print("hi")' in result[0]["content"]


def test_parse_code_block_without_language():
    md = "```\nsome code here\n```"
    result = parse(md)
    assert len(result) == 1
    assert result[0]["type"] == "code_block"
    assert result[0]["language"] == ""
    assert result[0]["content"] == "some code here"


def test_parse_unordered_list():
    md = "- First item\n- Second item\n- Third item"
    result = parse(md)
    assert len(result) == 1
    assert result[0]["type"] == "list"
    assert result[0]["ordered"] is False
    assert result[0]["items"] == ["First item", "Second item", "Third item"]


def test_parse_inline_bold_and_italic():
    md = "This has **bold** and *italic* text."
    result = parse(md)
    assert len(result) == 1
    assert result[0]["type"] == "paragraph"
    assert "**bold**" in result[0]["content"]
    assert "*italic*" in result[0]["content"]


def test_parse_heading_with_inline_formatting():
    md = "## A **bold** heading"
    result = parse(md)
    assert len(result) == 1
    assert result[0]["type"] == "heading"
    assert result[0]["level"] == 2
    assert result[0]["content"] == "A **bold** heading"


def test_parse_mixed_document():
    md = (
        "# My Document\n"
        "\n"
        "This is the introduction.\n"
        "\n"
        "## Features\n"
        "\n"
        "- Fast parsing\n"
        "- Easy to use\n"
        "- Lightweight\n"
        "\n"
        "```python\nimport parser\nparser.run()\n```\n"
        "\n"
        "That is all."
    )
    result = parse(md)
    assert len(result) == 6
    assert result[0]["type"] == "heading"
    assert result[0]["content"] == "My Document"
    assert result[1]["type"] == "paragraph"
    assert result[2]["type"] == "heading"
    assert result[2]["content"] == "Features"
    assert result[3]["type"] == "list"
    assert len(result[3]["items"]) == 3
    assert result[4]["type"] == "code_block"
    assert result[4]["language"] == "python"
    assert result[5]["type"] == "paragraph"
    assert result[5]["content"] == "That is all."


def test_parse_empty_input():
    result = parse("")
    assert result == []
