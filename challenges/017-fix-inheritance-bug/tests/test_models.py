"""Tests for Challenge 017: Fix the Inheritance Bugs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from models import BaseDocument, EditableDocument, VersionedDocument, PublishedDocument


# --- BaseDocument ---

def test_base_document_creation():
    doc = BaseDocument("Test", "Hello world")
    assert doc.title == "Test"
    assert doc.content == "Hello world"
    assert doc.created_at is not None


def test_base_document_summary():
    doc = BaseDocument("Title", "Short content")
    assert doc.summary() == "Title: Short content"


# --- EditableDocument ---

def test_editable_has_base_attributes():
    doc = EditableDocument("My Doc", "Initial content", author="Alice")
    assert doc.title == "My Doc"
    assert doc.content == "Initial content"
    assert doc.created_at is not None
    assert doc.last_editor == "Alice"


def test_editable_edit():
    doc = EditableDocument("Doc", "v1", author="Alice")
    doc.edit("v2", "Bob")
    assert doc.content == "v2"
    assert doc.last_editor == "Bob"
    assert doc.edit_count == 1
    assert len(doc.edit_history) == 1


# --- VersionedDocument ---

def test_versioned_has_all_attributes():
    doc = VersionedDocument("Spec", "Draft", author="Carol")
    assert doc.title == "Spec"
    assert doc.content == "Draft"
    assert doc.version == 1
    assert doc.last_editor == "Carol"


def test_versioned_edit_bumps_version():
    doc = VersionedDocument("Spec", "v1", author="Carol")
    doc.edit("v2", "Dave", change_note="Updated intro")
    assert doc.version == 2
    assert doc.content == "v2"
    assert doc.edit_count == 1
    assert len(doc.changelog) == 1


def test_versioned_get_version_info():
    doc = VersionedDocument("Spec", "v1", author="Carol")
    info = doc.get_version_info()
    assert info["title"] == "Spec"
    assert info["version"] == 1
    assert info["total_edits"] == 0


# --- PublishedDocument ---

def test_published_has_all_attributes():
    doc = PublishedDocument("Release Notes", "Content here", author="Eve")
    assert doc.title == "Release Notes"
    assert doc.content == "Content here"
    assert doc.version == 1
    assert doc.published is False


def test_published_publish():
    doc = PublishedDocument("Notes", "Content", author="Eve")
    doc.publish()
    assert doc.published is True
    assert doc.publish_date is not None


def test_published_status():
    doc = PublishedDocument("Notes", "Some words here", author="Eve")
    status = doc.status()
    assert status["title"] == "Notes"
    assert status["published"] is False
    assert status["word_count"] == 3
    assert status["version"] == 1
