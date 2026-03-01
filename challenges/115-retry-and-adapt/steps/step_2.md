# Step 2: Adapt and Fix

Your previous attempt has been tested. Here are the results:

- **test_basic_grouping: PASSED**
- **test_empty_input: FAILED** -- your function crashes on empty list instead of returning `{}`
- **test_missing_category: FAILED** -- records without a `category` field crash your function instead of being placed in `"uncategorized"`
- **test_non_numeric_values: FAILED** -- records with `value="N/A"` crash instead of being skipped
- **test_single_category: PASSED**

Review these results and your notes in `setup/attempt_log.json`. Fix your implementation in `setup/solution.py` to handle ALL edge cases.

Hints:
- Not all records have a `category` key -- use `.get()` with a default
- Not all `value` fields are numeric -- check before including in averages
- An empty list is a valid input
