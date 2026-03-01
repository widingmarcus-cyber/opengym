"""Template renderer that inserts user data into templates."""


def render_template(template, user_data):
    """Render a template string with user-provided data.

    Args:
        template: A string with {key} placeholders.
        user_data: A dictionary of key-value pairs to insert.

    Returns:
        The rendered string.
    """
    return template.format(**user_data)
