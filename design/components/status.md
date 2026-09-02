# Status

A status communicates an actual run or verifier state. Do not use status formatting for ordinary metadata.

## Semantic mapping

| State | Treatment |
| --- | --- |
| Successful, completed | Success foreground and subtle background |
| Queued, running, attention required | Warning foreground and subtle background |
| Failed | Danger foreground and subtle background |
| Inactive, pending, unknown | Neutral foreground and subtle background |

Use matching text, subtle-background, and border tokens. The label must name the state. Color is a secondary cue.

Use `--rs-radius-control`. Do not use a pill radius.

## Counts

Put run counts next to their labels. Use tabular numerals. Do not create one card for each status.

## Dynamic state

Use a live region for an important asynchronous change. Do not announce each status poll.

Do not animate status for decoration. Keep status text readable when a row is selected.
