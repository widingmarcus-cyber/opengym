# Challenge 209: Write Ack Lost

## Difficulty: Hard
## Category: Failure Recovery

## Description

A batch write operation sent 12 records to a simulated data store. The write acknowledgments were partially lost due to a network hiccup. The client does not know which writes actually succeeded.

Files:
- `setup/write_requests.json` — the 12 records that were sent for writing
- `setup/ack_log.json` — partial acknowledgment log (only some writes were acknowledged)
- `setup/data_store.json` — the actual state of the data store (ground truth of what was persisted)

Your job:
1. Compare the write requests against the actual data store to determine which writes succeeded.
2. Identify writes that succeeded but were not acknowledged (lost acks).
3. Identify writes that were acknowledged but are NOT in the store (false acks — should not exist here but verify).
4. Retry any writes that did NOT succeed (append them to the data store).
5. Produce a complete, verified data store at `setup/data_store_verified.json`.
6. Write a reconciliation report at `setup/reconciliation_report.json`.

## Expected Output

- `setup/data_store_verified.json` — all 12 records present and verified
- `setup/reconciliation_report.json` — JSON with keys: `total_writes` (12), `acked_writes` (int), `actual_persisted` (int), `lost_acks` (list of record IDs), `missing_writes` (list of record IDs that needed retry), `false_acks` (list, should be empty), `all_verified` (true)

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
