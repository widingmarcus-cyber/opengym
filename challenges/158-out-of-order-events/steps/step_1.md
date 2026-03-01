You are the Sorter agent. Your task is to reorder out-of-order events.

1. Read `setup/events.json`. It contains 5 events with `seq` (sequence number) and `data` fields. The events are delivered out of order.
2. Sort the events by their `seq` field in ascending order (1, 2, 3, 4, 5).
3. Write the sorted array to `setup/ordered.json`.

Expected output in ordered.json:
```json
[
  {"seq": 1, "data": "alpha"},
  {"seq": 2, "data": "beta"},
  {"seq": 3, "data": "gamma"},
  {"seq": 4, "data": "delta"},
  {"seq": 5, "data": "epsilon"}
]
```
