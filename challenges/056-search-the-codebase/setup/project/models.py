"""Data models for the application."""

from datetime import datetime


class User:
    """Represents a user in the system."""

    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.created_at = datetime.now()

    def to_dict(self):
        """Convert user to dictionary."""
        return {
            "id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }


class Post:
    """Represents a blog post."""

    def __init__(self, post_id, title, content, author_id):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at = datetime.now()

    def to_dict(self):
        """Convert post to dictionary."""
        return {
            "id": self.post_id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat(),
        }

    def summary(self):
        """Return a short summary of the post."""
        return self.content[:100] if len(self.content) > 100 else self.content


class Comment:
    """Represents a comment on a post."""

    def __init__(self, comment_id, post_id, author_id, text):
        self.comment_id = comment_id
        self.post_id = post_id
        self.author_id = author_id
        self.text = text

    def to_dict(self):
        """Convert comment to dictionary."""
        return {
            "id": self.comment_id,
            "post_id": self.post_id,
            "author_id": self.author_id,
            "text": self.text,
        }
