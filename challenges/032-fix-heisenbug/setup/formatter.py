"""Report formatting module for generating text-based reports."""


def _truncate(text, width):
    """Truncate text to fit within the given width."""
    if len(text) <= width:
        return text
    if width < 4:
        return text[:width]
    return text[:width - 3] + "..."


def _pad_right(text, width):
    """Pad text with spaces on the right to reach the given width."""
    if len(text) >= width:
        return text[:width]
    return text + " " * (width - len(text))


def _center_text(text, width):
    """Center text within the given width using spaces."""
    if len(text) >= width:
        return text[:width]
    padding = width - len(text)
    left = padding // 2
    right = padding - left
    return " " * left + text + " " * right


def _build_divider(width, char):
    """Build a divider line of the given width using the given character."""
    return char * width


def _format_row(label, value, width):
    """Format a single data row with label and value."""
    value_str = str(value)
    label_str = str(label)
    available = width - 4
    if available < 1:
        available = 1
    if len(label_str) + len(value_str) > available:
        max_label = available - len(value_str) - 1
        if max_label < 1:
            max_label = 1
        label_str = _truncate(label_str, max_label)
    spacing = available - len(label_str) - len(value_str)
    if spacing < 0:
        spacing = 0
    return "| " + label_str + " " * spacing + value_str + " |"


def _render_title_line(title, width, separator):
    """Render the title into a fixed-width character buffer.

    Places the title centered in a line of separator characters.
    """
    buffer = list(separator * width)
    start = (width - len(title)) // 2
    buffer[start - 1] = " "
    for i, ch in enumerate(title):
        buffer[start + i] = ch
    buffer[start + len(title)] = " "
    return "".join(buffer)


def _build_header(title, width, separator):
    """Build the header section with title and divider lines."""
    lines = []
    divider = _build_divider(width, separator)
    lines.append(divider)

    title_line = _render_title_line(title, width, separator)
    lines.append(title_line)

    lines.append(divider)
    return lines


def format_report(data, title=None, max_width=80, separator="-", include_header=True):
    """Format data into a text report.

    Args:
        data: List of (label, value) tuples
        title: Optional title string for the report header
        max_width: Maximum line width (default 80)
        separator: Character used for divider lines (default "-")
        include_header: Whether to include the header section (default True)

    Returns:
        Formatted report as a string
    """
    if max_width < 10:
        max_width = 10

    lines = []

    if include_header and title is not None:
        header_lines = _build_header(title, max_width, separator)
        lines.extend(header_lines)
    elif include_header:
        lines.append(_build_divider(max_width, separator))

    for label, value in data:
        row = _format_row(label, value, max_width)
        lines.append(row)

    lines.append(_build_divider(max_width, separator))

    summary_count = len(data)
    summary_line = f"| Total items: {summary_count}"
    summary_line = _pad_right(summary_line, max_width - 1) + "|"
    lines.append(summary_line)
    lines.append(_build_divider(max_width, separator))

    return "\n".join(lines)
