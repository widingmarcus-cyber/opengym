# Challenge 190: Zombie Session Cleanup

**Difficulty:** medium
**Category:** task-sequencing
**Dimension:** planning
**Type:** single-session

## Description

Your system has sessions that should complete within minutes, but some have been stuck in "running" status for over 24 hours. These are zombie sessions that need to be identified and terminated.

The current time is `2024-01-02T00:00:00Z`. Any session still marked as "running" that started before `2024-01-01T00:00:00Z` (more than 24 hours ago) is considered a zombie.

## Objectives

- Read `setup/sessions.json` which contains session records.
- Identify zombie sessions (status="running" for more than 24 hours).
- Update `setup/sessions.json`: change the status of zombie sessions to "terminated".
- Write `setup/answer.json` with the count of zombies found and their IDs.

## Expected Output

`setup/answer.json`:
```json
{
  "zombies_found": 2,
  "terminated": ["s2", "s4"]
}
```

Updated `setup/sessions.json` should have s2 and s4 with status "terminated".
