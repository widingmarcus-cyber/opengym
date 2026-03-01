# Challenge 085: Build Markdown Parser

## Difficulty: Medium

## Task

Build a Markdown parser that converts Markdown text into a structured list of block elements. Implement the parser in `setup/md_parser.py`.

## Requirements

Implement this function in `setup/md_parser.py`:

1. `parse(markdown_text)` -- Parse a Markdown string and return a list of dictionaries, where each dictionary represents a block-level element.

### Supported Block Types

- **Headings**: Lines starting with `#` (1-6 levels). Output: `{"type": "heading", "level": <int>, "content": "<text>"}`.

- **Paragraphs**: Consecutive non-empty lines that are not other block types. Output: `{"type": "paragraph", "content": "<text>"}`.

- **Code blocks**: Fenced with triple backticks. An optional language identifier may follow the opening backticks. Output: `{"type": "code_block", "language": "<lang or empty string>", "content": "<code>"}`.

- **Unordered lists**: Lines starting with `- `. Consecutive list items form a single list block. Output: `{"type": "list", "ordered": False, "items": ["item1", "item2", ...]}`.

### Inline Formatting

Within `content` fields of headings and paragraphs, preserve inline markers as-is:
- `**bold**` stays as `**bold**`
- `*italic*` stays as `*italic*`

These markers should remain in the content string; do not strip or transform them.

### Parsing Rules

- Blocks are separated by blank lines
- Code block content preserves internal newlines exactly
- Leading `# ` markers are stripped from heading content
- Leading `- ` markers are stripped from list item text

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules
- Do not use any Markdown parsing libraries
