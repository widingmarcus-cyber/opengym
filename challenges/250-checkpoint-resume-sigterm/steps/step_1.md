# Step 1: Process Records

Process all 20 records from `setup/records.json`. For each record, apply the transformation rules from `setup/rules.json` and write processed records to `setup/output.json`.

Save your progress to `setup/checkpoint.json` after processing each record so you can resume if interrupted. The checkpoint should track which record IDs have been processed and their transformed values.

Your process may be interrupted by a SIGTERM signal. Ensure your checkpoint is written frequently enough that minimal work is lost on interruption.
