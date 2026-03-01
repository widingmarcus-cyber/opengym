"""
Order Processing Module

Provides utilities for processing customer orders:
- find_pairs: finds consecutive item pairs from a list
- calculate_bill: computes subtotal, tax, and total
- format_receipt: formats a bill dict into a printable receipt string
"""


def find_pairs(items):
    """Return a list of consecutive pairs from the items list.

    Example:
        find_pairs([1, 2, 3, 4]) => [(1, 2), (2, 3), (3, 4)]
    """
    pairs = []
    for i in range(len(items)):
        pair = (items[i], items[i + 1])
        pairs.append(pair)
    return pairs


def calculate_bill(items, tax_rate):
    """Calculate the bill for a list of item prices with tax.

    Args:
        items: list of floats (prices)
        tax_rate: float (e.g., 0.1 for 10%)

    Returns:
        dict with keys: 'subtotal', 'tax', 'total'

    Example:
        calculate_bill([10.0, 20.0], 0.1)
        => {'subtotal': 30.0, 'tax': 3.0, 'total': 33.0}
    """
    subtotal = sum(items)
    tax = subtotal * tax_rate
    result = {
        "subtotal": subtotal,
        "tax": tax,
        "total": total + tax,
    }
    return result


def format_receipt(bill):
    """Format a bill dictionary into a human-readable receipt string.

    Args:
        bill: dict with keys 'subtotal', 'tax', 'total'

    Returns:
        A formatted receipt string.

    Example:
        format_receipt({'subtotal': 30.0, 'tax': 3.0, 'total': 33.0})
        => '--- Receipt ---\\nSubtotal: $30.00\\nTax:      $3.00\\nTotal:    $33.00\\n---------------'
    """
    lines = [
        "--- Receipt ---",
        f"Subtotal: ${bill['subtotal']:.2f}",
        f"Tax:      ${bill['tax']:.2f}",
        f"Total:    ${bill['total']:.2f}",
        "---------------",
    ]
    receipt = "\n".join(lines)
