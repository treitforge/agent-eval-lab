# Typography

## Family

Use `--rs-font-sans`, a restrained system sans-serif stack, for the interface. Use
`--rs-font-mono` only for candidate IDs, hashes, commands, timestamps, job IDs, and other
machine-oriented values. Repository names remain sans-serif.

## Scale

| Purpose | Token | Size |
| --- | --- | --- |
| Page title | `--rs-type-page` or `--rs-type-page-compact` | 24px or 20px |
| Primary interface text | `--rs-type-body` | 14px |
| Dense metadata | `--rs-type-meta` | 13px |
| Table header and compact metadata | `--rs-type-label` | 12px |

A screen should normally use approximately three sizes. Prefer weight and spacing over a new
size. Use `--rs-weight-*` and `--rs-leading-*` tokens rather than raw values.

## Rules

- Use sentence case by default.
- Do not repeat uppercase eyebrow labels above ordinary sections.
- Table headers may use compact weight and tracking, but must remain easy to scan.
- Use `--rs-numerals-tabular` for counts and numeric columns.
- Keep line length controlled in rationale and evidence prose.
- Do not use typography as decoration or introduce a display face.
