# Step 2: Fix the Bugs Using Your Notes

The file `setup/buggy_app.py` contains 3 bugs — one in each function.

Your notes from the previous session are saved in `setup/notes.md`. Read your notes and use them to fix all 3 bugs in `setup/buggy_app.py`.

After fixing, the functions should behave as follows:

- `find_pairs([1, 2, 3, 4])` returns `[(1, 2), (2, 3), (3, 4)]` without raising an error
- `calculate_bill([10.0, 20.0], 0.1)` returns `{'subtotal': 30.0, 'tax': 3.0, 'total': 33.0}`
- `format_receipt(bill_dict)` returns a non-empty string (not `None`)
