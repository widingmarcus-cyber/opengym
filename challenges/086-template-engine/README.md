# Challenge 086: Template Engine

## Difficulty: Medium

## Task

Build a simple template engine that supports variable substitution, conditionals, and loops. Implement the engine in `setup/template.py`.

## Requirements

Implement this function in `setup/template.py`:

1. `render(template_str, context)` -- Render a template string using the provided context dictionary and return the resulting string.

### Template Syntax

- **Variable substitution**: `{{variable}}` is replaced with the value of `variable` from the context. Supports dot notation for nested access: `{{user.name}}` accesses `context["user"]["name"]`.

- **Conditionals**: `{% if condition %}...{% else %}...{% endif %}`. The `{% else %}` block is optional. The condition is a variable name (or dot-notation path) evaluated for truthiness.

- **Loops**: `{% for item in list %}...{% endfor %}`. Iterates over a list from the context. Inside the loop body, `{{item}}` refers to the current element.

### Behavior

- Missing variables should render as an empty string (no errors).
- Whitespace within tags is flexible: `{{ name }}` and `{{name}}` should both work.
- Nested structures (e.g., a loop inside a conditional) must be supported.

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules
- Do not use Jinja2, Mako, or any external template libraries
