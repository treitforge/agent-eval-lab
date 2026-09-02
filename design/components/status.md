# Status

Status communicates an actual workflow state, never a category that plain text can express.

## Semantic mapping

| State | Treatment |
| --- | --- |
| Accepted, completed | Success foreground and subtle background |
| Held, queued, running, attention required | Warning foreground and subtle background |
| Rejected, failed | Danger foreground and subtle background |
| Inactive, pending, unknown | Neutral foreground and subtle background |

Use the matching `--rs-color-*-text`, `--rs-color-*-subtle`, and border tokens. The label must
name the state; color is supplementary. Use `--rs-radius-control`, not a pill radius.

## Counts

Workflow counts belong inline with status tabs. Use tabular numerals. Do not create one card per
status and do not emphasize a count unless it changes a reviewer decision.

## Dynamic state

Use an appropriate live region for meaningful asynchronous changes, without announcing every
poll. Do not animate status decoratively. Preserve readable text when a row is selected.
