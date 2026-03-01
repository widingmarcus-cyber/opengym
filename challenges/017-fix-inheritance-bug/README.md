# Challenge 017: Fix the Inheritance Bugs

## Difficulty: Hard

## Task

The file `setup/models.py` implements a class hierarchy for a document management system:

- `BaseDocument` -- Base class with common attributes (title, content, created_at)
- `EditableDocument(BaseDocument)` -- Adds editing capabilities (edit history, last_editor)
- `VersionedDocument(EditableDocument)` -- Adds version control (version number, changelog)
- `PublishedDocument(VersionedDocument)` -- Adds publishing features (published flag, publish_date)

The hierarchy has several inheritance-related bugs:

- `__init__` methods that fail to call `super().__init__()` correctly, causing missing attributes
- A method call that fails to pass `self` correctly through the inheritance chain
- `__repr__` methods that reference attributes from the parent that were never initialized

**Your job:** Fix all inheritance issues so the class hierarchy works correctly.

## Rules

- Only modify files in the `setup/` directory
- Do not change the class names or public method signatures
- Do not remove any existing classes
- The inheritance chain must remain: BaseDocument -> EditableDocument -> VersionedDocument -> PublishedDocument
