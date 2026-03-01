# Step 2: Retrieve Fact 137

Your memory is stored across 4 page files in `setup/memory/`:
- `page_1.json` -- facts 1 through 50
- `page_2.json` -- facts 51 through 100
- `page_3.json` -- facts 101 through 150
- `page_4.json` -- facts 151 through 200

Determine which page contains **fact number 137**. Read that page file and extract the text of fact 137.

Write only the fact text (not the number prefix) to `setup/answer.txt`.

For example, if fact 137 were "The sky is blue", you would write exactly:
```
The sky is blue
```

No quotes, no "Fact 137:" prefix, no extra whitespace.
