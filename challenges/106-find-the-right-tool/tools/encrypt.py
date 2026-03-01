#!/usr/bin/env python3
"""Encrypt a file using a simple XOR cipher."""

import argparse
import sys
import os


def xor_encrypt(data, key):
    """XOR encrypt data with the given key."""
    key_bytes = key.encode("utf-8")
    return bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data))


def main():
    parser = argparse.ArgumentParser(
        description="Encrypt a file using XOR cipher with the given key"
    )
    parser.add_argument("input_file", help="Path to the file to encrypt")
    parser.add_argument("--key", required=True, help="Encryption key string")
    parser.add_argument(
        "-o", "--output", help="Output file path (default: input_file.enc)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or args.input_file + ".enc"

    with open(args.input_file, "rb") as f:
        data = f.read()

    encrypted = xor_encrypt(data, args.key)

    with open(output_path, "wb") as f:
        f.write(encrypted)

    print(f"Encrypted '{args.input_file}' -> '{output_path}' with key '{args.key}'")


if __name__ == "__main__":
    main()
