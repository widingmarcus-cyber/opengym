# Step 2: Process Transactions with Rollback

Read `setup/state.json` and `setup/history.json`. Process the following two transactions in order:

## Transaction 1: Withdraw 30
- Current balance is 100. Withdrawing 30 is valid (30 <= 100).
- Update the state: set balance to 70, append `{"type": "withdraw", "amount": 30}` to the transactions list.
- Save a snapshot: append `{"version": 2, "state": {"balance": 70, "transactions": [{"type": "withdraw", "amount": 30}]}}` to `setup/history.json`.
- Write the updated state to `setup/state.json`.

## Transaction 2: Withdraw 200
- Current balance is 70. Withdrawing 200 is INVALID (200 > 70 -- insufficient funds).
- This transaction MUST FAIL. Do NOT apply it.
- Since the transaction failed, ROLLBACK to the last successful state (version 2).
- Ensure `setup/state.json` contains the version 2 state: `{"balance": 70, "transactions": [{"type": "withdraw", "amount": 30}]}`.

After this step:
- `setup/state.json` should have balance=70 with 1 transaction.
- `setup/history.json` should have versions 1 and 2 (no version 3, since the failed transaction was rolled back).
