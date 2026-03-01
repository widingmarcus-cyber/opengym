"""String utility functions."""


def wrap_text(text, width):
    """Word-wrap text to the given width."""
    if not text:
        return ""
    if width <= 0:
        return text

    words = text.split()
    if not words:
        return ""

    lines = []
    current_line = words[0]

    for word in words[1:]:
        if len(current_line) + 1 + len(word) <= width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return "\n".join(lines)


def pad_center(text, width, char=" "):
    """Center text within the given width using the padding character."""
    if len(text) >= width:
        return text
    total_padding = width - len(text)
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding
    return char * left_padding + text + char * right_padding


def remove_duplicates(text):
    """Remove consecutive duplicate characters."""
    if not text:
        return ""
    result = [text[0]]
    for char in text[1:]:
        if char != result[-1]:
            result.append(char)
    return "".join(result)


def count_words(text):
    """Count the number of words in text."""
    return len(text.split())
