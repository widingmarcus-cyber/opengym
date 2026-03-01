# Step 1: Store Records Under Size Cap

You have 50 records to store. However, `setup/memory.json` must not exceed **1024 bytes** in total file size.

10 of the 50 records are marked **IMPORTANT** and must be prioritized. Store all IMPORTANT records. You may also store additional non-important records if space allows, but do not exceed the size cap.

Here are all 50 records:

| # | Key | Value |
|---|-----|-------|
| 1 | item_01 | general info about item 1 not critical |
| 2 | item_02 | general info about item 2 not critical |
| 3 | item_03 | **IMPORTANT: critical data for item 3** |
| 4 | item_04 | general info about item 4 not critical |
| 5 | item_05 | general info about item 5 not critical |
| 6 | item_06 | general info about item 6 not critical |
| 7 | item_07 | **IMPORTANT: critical data for item 7** |
| 8 | item_08 | general info about item 8 not critical |
| 9 | item_09 | general info about item 9 not critical |
| 10 | item_10 | general info about item 10 not critical |
| 11 | item_11 | general info about item 11 not critical |
| 12 | item_12 | **IMPORTANT: critical data for item 12** |
| 13 | item_13 | general info about item 13 not critical |
| 14 | item_14 | general info about item 14 not critical |
| 15 | item_15 | general info about item 15 not critical |
| 16 | item_16 | general info about item 16 not critical |
| 17 | item_17 | general info about item 17 not critical |
| 18 | item_18 | **IMPORTANT: critical data for item 18** |
| 19 | item_19 | general info about item 19 not critical |
| 20 | item_20 | general info about item 20 not critical |
| 21 | item_21 | general info about item 21 not critical |
| 22 | item_22 | general info about item 22 not critical |
| 23 | item_23 | **IMPORTANT: critical data for item 23** |
| 24 | item_24 | general info about item 24 not critical |
| 25 | item_25 | general info about item 25 not critical |
| 26 | item_26 | general info about item 26 not critical |
| 27 | item_27 | general info about item 27 not critical |
| 28 | item_28 | general info about item 28 not critical |
| 29 | item_29 | **IMPORTANT: critical data for item 29** |
| 30 | item_30 | general info about item 30 not critical |
| 31 | item_31 | general info about item 31 not critical |
| 32 | item_32 | general info about item 32 not critical |
| 33 | item_33 | general info about item 33 not critical |
| 34 | item_34 | **IMPORTANT: critical data for item 34** |
| 35 | item_35 | general info about item 35 not critical |
| 36 | item_36 | general info about item 36 not critical |
| 37 | item_37 | general info about item 37 not critical |
| 38 | item_38 | **IMPORTANT: critical data for item 38** |
| 39 | item_39 | general info about item 39 not critical |
| 40 | item_40 | general info about item 40 not critical |
| 41 | item_41 | general info about item 41 not critical |
| 42 | item_42 | **IMPORTANT: critical data for item 42** |
| 43 | item_43 | general info about item 43 not critical |
| 44 | item_44 | general info about item 44 not critical |
| 45 | item_45 | general info about item 45 not critical |
| 46 | item_46 | general info about item 46 not critical |
| 47 | item_47 | **IMPORTANT: critical data for item 47** |
| 48 | item_48 | general info about item 48 not critical |
| 49 | item_49 | general info about item 49 not critical |
| 50 | item_50 | general info about item 50 not critical |

Store the records as a JSON array to `setup/memory.json`. Each record should be an object with `key` and `value` fields. For example:

```json
[{"key": "item_03", "value": "IMPORTANT: critical data for item 3"}, ...]
```

**Constraint:** The total file size of `setup/memory.json` must not exceed 1024 bytes.

The file `setup/memory.json` will persist to the next session.
