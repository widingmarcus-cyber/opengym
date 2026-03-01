# Challenge 194: Daylight Savings Transition

**Difficulty:** hard
**Category:** task-sequencing
**Dimension:** planning
**Type:** single-session

## Description

Daylight Saving Time (DST) transitions can cause scheduled tasks to fail when a local time simply does not exist. On March 10, 2024 (US/Eastern), clocks spring forward from 2:00 AM to 3:00 AM. This means 2:30 AM never occurs.

A backup task is scheduled for 2:30 AM US/Eastern on that date. Your job is to detect the DST issue and determine an appropriate resolution.

## Objectives

- Read `setup/schedule.json` which contains a task scheduled during a DST gap.
- Detect that 2:30 AM US/Eastern on 2024-03-10 does not exist due to spring-forward.
- Write `setup/answer.json` acknowledging the issue and proposing a resolution.

## Expected Output

`setup/answer.json` should contain:
```json
{
  "task": "backup",
  "issue": "time_does_not_exist",
  "reason": "DST spring-forward: clocks skip from 2:00 AM to 3:00 AM on 2024-03-10 in US/Eastern",
  "resolution": "shift_to_0330",
  "utc_equivalent": null
}
```

The `issue` field must not be empty or null. The `resolution` can be "skip" or "shift_to_0330" (shift to 3:30 AM, the next valid time). Since the original time doesn't exist, `utc_equivalent` may be null or the shifted equivalent ("08:30:00Z" if shifted to 3:30 AM EDT).
