def summarize_records(records, group_by, count_field):
    """Group records by a field and count occurrences of each value.

    Args:
        records: list of dicts
        group_by: field name to group by
        count_field: field name to count unique values of

    Returns:
        dict mapping group_by values to count of unique count_field values

    Example:
        records = [
            {"city": "NYC", "dept": "Sales"},
            {"city": "NYC", "dept": "HR"},
            {"city": "NYC", "dept": "Sales"},
            {"city": "LA", "dept": "Sales"},
        ]
        summarize_records(records, "city", "dept")
        # Returns {"NYC": 2, "LA": 1}
    """
    pass
