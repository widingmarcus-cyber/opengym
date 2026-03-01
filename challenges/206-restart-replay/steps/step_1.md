# Step 1: Build WAL and Execute Operations

## Task

You have a bank account ledger starting from `setup/initial_ledger.json`. Apply the operations listed in `setup/operations.json` using a Write-Ahead Log pattern:

1. Read `setup/initial_ledger.json` — a dict of `account_id -> balance`.
2. For each operation in `setup/operations.json`:
   - First, write the operation to the WAL (`setup/wal.json`) BEFORE applying it
   - Then apply the operation to the ledger
   - Operations are: `deposit(account, amount)`, `withdraw(account, amount)`, `transfer(from, to, amount)`
3. After all operations, save:
   - `setup/wal.json` — array of all WAL entries, each with: `seq` (sequence number starting at 1), `op` (operation type), `params` (operation parameters), `applied` (true)
   - `setup/state.json` — the final ledger state: `{"ledger": {account_id: balance}, "wal_length": N}`

The "crash" happens here. Only wal.json and state.json survive.
