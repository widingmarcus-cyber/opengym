"""Document management class hierarchy."""

from datetime import datetime


class BaseDocument:
    """Base class for all documents."""

    def __init__(self, title, content=""):
        self.title = title
        self.content = content
        self.created_at = datetime.now()

    def summary(self):
        """Return a short summary of the document."""
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"{self.title}: {preview}"

    def word_count(self):
        """Return the number of words in the content."""
        return len(self.content.split())

    def __repr__(self):
        return f"BaseDocument(title={self.title!r})"


class EditableDocument(BaseDocument):
    """A document that tracks edit history."""

    def __init__(self, title, content="", author="unknown"):
        self.last_editor = author
        self.edit_count = 0
        self.edit_history = []

    def edit(self, new_content, editor):
        """Edit the document content."""
        self.edit_history.append({
            "old_content": self.content,
            "editor": editor,
            "timestamp": datetime.now(),
        })
        self.content = new_content
        self.last_editor = editor
        self.edit_count += 1

    def __repr__(self):
        return f"EditableDocument(title={self.title!r}, edits={self.edit_count})"


class VersionedDocument(EditableDocument):
    """A document with version control."""

    def __init__(self, title, content="", author="unknown"):
        self.version = 1
        self.changelog = []

    def edit(self, new_content, editor, change_note=""):
        """Edit the document and bump the version."""
        self.changelog.append({
            "version": self.version,
            "note": change_note,
            "editor": editor,
        })
        self.version += 1
        EditableDocument.edit(new_content, editor)

    def get_version_info(self):
        """Return current version information."""
        return {
            "title": self.title,
            "version": self.version,
            "total_edits": self.edit_count,
            "last_editor": self.last_editor,
        }

    def __repr__(self):
        return f"VersionedDocument(title={self.title!r}, v{self.version})"


class PublishedDocument(VersionedDocument):
    """A document that can be published."""

    def __init__(self, title, content="", author="unknown"):
        self.published = False
        self.publish_date = None

    def publish(self):
        """Mark the document as published."""
        if self.version < 1:
            raise ValueError("Cannot publish a document with no version")
        self.published = True
        self.publish_date = datetime.now()

    def unpublish(self):
        """Unpublish the document."""
        self.published = False
        self.publish_date = None

    def status(self):
        """Return the document status."""
        return {
            "title": self.title,
            "version": self.version,
            "published": self.published,
            "word_count": self.word_count(),
        }

    def __repr__(self):
        state = "published" if self.published else "draft"
        return f"PublishedDocument(title={self.title!r}, v{self.version}, {state})"
