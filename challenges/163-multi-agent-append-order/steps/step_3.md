You are Agent C. Your task is to append the third line to the shared log file and count the total lines.

1. Read `setup/log.txt` (should contain Agent A's and Agent B's lines).
2. Append the following line (do NOT overwrite previous lines):

```
C:step3
```

3. Count the total number of lines in the file (should be 3).
4. Write the count as a string to `setup/answer.txt`.

After this step, log.txt should contain:
```
A:step1
B:step2
C:step3
```

And answer.txt should contain:
```
3
```

IMPORTANT: You MUST preserve all existing lines. Append only, do not overwrite.
