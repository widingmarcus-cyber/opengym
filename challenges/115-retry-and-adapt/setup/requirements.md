# Data Processor Requirements

## Function: `process_data(records)`

### Input
- `records`: A list of dictionaries. Each dict may contain:
  - `category` (str): The category to group by. **May be missing.**
  - `value` (numeric or other): The value to average. **May be non-numeric.**

### Output
- A dictionary mapping each category (str) to the average value (float) of all valid numeric records in that category.

### Rules
1. Group records by their `category` field
2. Calculate the average `value` for each category
3. Records without a `category` field should be grouped under `"uncategorized"`
4. Records with non-numeric `value` fields (e.g., `"N/A"`, `None`) should be **skipped** when calculating averages
5. If a category has no valid numeric values after filtering, it should not appear in the output
6. An empty input list should return an empty dictionary `{}`
7. All average values should be floats

### Examples

```python
# Basic grouping
process_data([
    {"category": "A", "value": 10},
    {"category": "A", "value": 20},
    {"category": "B", "value": 30},
])
# Returns: {"A": 15.0, "B": 30.0}

# Missing category
process_data([{"value": 10}])
# Returns: {"uncategorized": 10.0}

# Non-numeric value skipped
process_data([
    {"category": "A", "value": 10},
    {"category": "A", "value": "N/A"},
])
# Returns: {"A": 10.0}
```
