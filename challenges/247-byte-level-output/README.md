# Challenge 247: Precise Byte-Level Output

**Dimension:** Resilience
**Category:** Fault-tolerance
**Difficulty:** Hard

## Objective

Apply a series of transformation rules to an input file and produce 3 output files that match their expected SHA256 checksums exactly. Precision matters -- every byte counts.

## Instructions

1. Read the transformation rules from `setup/rules.json`. The rules form a DAG (directed acyclic graph) with dependency ordering.

2. Read the input data from `setup/input.txt` (30 lines of `key:value` data).

3. Execute the rules in dependency order:
   - **rule_1** `normalize_whitespace`: Strip leading and trailing whitespace from each line. No dependencies.
   - **rule_2** `lowercase_values`: Lowercase the value part of each line (the part after the first `:`). The key stays as-is. Depends on rule_1.
   - **rule_3** `deduplicate`: Remove duplicate lines, keeping only the first occurrence. Depends on rule_2.
   - **rule_4** `sort_lines`: Sort all lines alphabetically (standard string sort). Depends on rule_3.
   - **rule_5** `extract_names`: From the sorted+deduped data, extract lines where the key is `name`, and write only the values (one per line) to `setup/outputs/names.txt`. Depends on rule_4.
   - **rule_6** `extract_numbers`: Extract lines where the value is numeric (keys: `amount`, `priority`), and write them in `key:value` format sorted by numeric value ascending to `setup/outputs/numbers.txt`. Depends on rule_4.
   - **rule_7** `extract_dates`: Extract lines where the key is `date`, and write only the date values sorted chronologically (ascending) to `setup/outputs/dates.txt`. Depends on rule_4.

4. Each output file must match its expected SHA256 checksum listed in `setup/manifest.json`.

## Output Files

- `setup/outputs/names.txt` — One name per line, newline-terminated.
- `setup/outputs/numbers.txt` — One `key:value` per line, sorted by numeric value ascending, newline-terminated.
- `setup/outputs/dates.txt` — One date per line, sorted chronologically, newline-terminated.

## Constraints

- Output files must end with a trailing newline.
- Use Unix-style line endings (`\n`, not `\r\n`).
- No trailing spaces on any line.
- The SHA256 checksums in the manifest are authoritative. Your output must match byte-for-byte.

## Verification

The verify script will re-derive the expected outputs from the input using the same rules and compare SHA256 checksums against both the manifest and your output files.
