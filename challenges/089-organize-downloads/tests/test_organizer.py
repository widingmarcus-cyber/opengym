"""Tests for Challenge 089: Organize Downloads."""

import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from organizer import organize


def _create_files(directory, filenames):
    os.makedirs(directory, exist_ok=True)
    for name in filenames:
        with open(os.path.join(directory, name), "w") as f:
            f.write(f"content of {name}")


def test_documents_category():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        _create_files(src, ["report.pdf", "notes.txt", "readme.md"])
        result = organize(src, tgt)
        assert "documents" in result
        assert sorted(result["documents"]) == ["notes.txt", "readme.md", "report.pdf"]
        for name in ["notes.txt", "readme.md", "report.pdf"]:
            assert os.path.isfile(os.path.join(tgt, "documents", name))


def test_images_category():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        _create_files(src, ["photo.jpg", "diagram.png"])
        result = organize(src, tgt)
        assert "images" in result
        assert sorted(result["images"]) == ["diagram.png", "photo.jpg"]


def test_code_category():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        _create_files(src, ["style.css", "index.html", "script.py"])
        result = organize(src, tgt)
        assert "code" in result
        assert sorted(result["code"]) == ["index.html", "script.py", "style.css"]


def test_media_and_data_categories():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        _create_files(src, ["song.mp3", "video.mp4", "data.csv"])
        result = organize(src, tgt)
        assert "media" in result
        assert sorted(result["media"]) == ["song.mp3", "video.mp4"]
        assert "data" in result
        assert result["data"] == ["data.csv"]


def test_archives_category():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        _create_files(src, ["archive.zip", "backup.tar", "compressed.gz"])
        result = organize(src, tgt)
        assert "archives" in result
        assert sorted(result["archives"]) == ["archive.zip", "backup.tar", "compressed.gz"]


def test_other_category():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        _create_files(src, ["app.exe", "mystery.dat"])
        result = organize(src, tgt)
        assert "other" in result
        assert sorted(result["other"]) == ["app.exe", "mystery.dat"]


def test_files_are_moved_not_copied():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        _create_files(src, ["report.pdf", "photo.jpg"])
        organize(src, tgt)
        assert not os.path.isfile(os.path.join(src, "report.pdf"))
        assert not os.path.isfile(os.path.join(src, "photo.jpg"))
        assert os.path.isfile(os.path.join(tgt, "documents", "report.pdf"))
        assert os.path.isfile(os.path.join(tgt, "images", "photo.jpg"))


def test_full_organization():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        all_files = [
            "report.pdf", "photo.jpg", "data.csv", "notes.txt", "app.exe",
            "style.css", "index.html", "script.py", "song.mp3", "video.mp4",
            "archive.zip", "diagram.png", "presentation.pptx", "spreadsheet.xlsx",
            "readme.md",
        ]
        _create_files(src, all_files)
        result = organize(src, tgt)

        assert sorted(result["documents"]) == [
            "notes.txt", "presentation.pptx", "readme.md", "report.pdf", "spreadsheet.xlsx"
        ]
        assert sorted(result["images"]) == ["diagram.png", "photo.jpg"]
        assert sorted(result["code"]) == ["index.html", "script.py", "style.css"]
        assert sorted(result["media"]) == ["song.mp3", "video.mp4"]
        assert result["data"] == ["data.csv"]
        assert result["archives"] == ["archive.zip"]
        assert result["other"] == ["app.exe"]

        remaining = os.listdir(src)
        assert len(remaining) == 0
