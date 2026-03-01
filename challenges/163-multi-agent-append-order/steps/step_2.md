You are Agent B. Your task is to append the second line to the shared log file.

1. Read `setup/log.txt` (should contain Agent A's line).
2. Append the following line (do NOT overwrite Agent A's line):

```
B:step2
```

After this step, the file should contain exactly 2 lines:
```
A:step1
B:step2
```

IMPORTANT: You MUST preserve Agent A's existing line. Append only, do not overwrite.
