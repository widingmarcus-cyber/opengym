def run_pipeline(raw_text, config_path, group_by, count_field, filter_field=None, filter_value=None):
    """Run the full pipeline.

    1. Load and validate config from config_path (YAML)
    2. Parse records from raw_text using phase1_fix.parse_records
    3. Optionally filter records using phase1_fix.filter_records
    4. Summarize using phase2_implement.summarize_records
    5. Return dict with keys: "config", "record_count", "summary", "enabled_features"

    - "config" = the loaded config dict
    - "record_count" = number of records after filtering
    - "summary" = result of summarize_records
    - "enabled_features" = list of feature names where enabled is true
    """
    pass
