#!/usr/bin/env python3
"""A mystery data processing tool. No documentation provided."""

import sys


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--version":
            print("1.0.0")
            sys.exit(0)
        elif arg in ("--help", "-h"):
            print("Usage: pipe text into this tool")
            sys.exit(0)
        # All other flags are silently ignored

    # Check if stdin has data
    if sys.stdin.isatty():
        print("Usage: pipe text into this tool")
        sys.exit(0)

    for line in sys.stdin:
        line = line.rstrip("\n").rstrip("\r")
        if not line:
            print()
            continue

        words = line.split()
        # Reverse the order of words
        reversed_words = words[::-1]
        # Capitalize the first word (which was the last word originally)
        if reversed_words:
            reversed_words[0] = reversed_words[0][0].upper() + reversed_words[0][1:]
        print(" ".join(reversed_words))


if __name__ == "__main__":
    main()
