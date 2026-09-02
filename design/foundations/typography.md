# Typography

## Family

Use `--rs-font-sans` for interface text. Use `--rs-font-mono` only for machine values.

Machine values include hashes, commands, timestamps, job identifiers, and source references. Keep model and agent names in the sans-serif font.

## Scale

| Purpose | Token | Size |
| --- | --- | --- |
| Page title | `--rs-type-page` or `--rs-type-page-compact` | 24px or 20px |
| Primary interface text | `--rs-type-body` | 14px |
| Dense metadata | `--rs-type-meta` | 13px |
| Table header and compact metadata | `--rs-type-label` | 12px |

Use approximately three text sizes on one screen. Use weight and spacing before you add a size.

Use `--rs-weight-*` and `--rs-leading-*` tokens. Do not use raw values.

## Rules

- Use sentence case by default.
- Do not repeat uppercase eyebrow labels above ordinary sections.
- Table headers can use compact weight and tracking. They must remain easy to scan.
- Use `--rs-numerals-tabular` for counts and numeric columns.
- Keep rationale and evidence lines at a readable length.
- Do not use typography as decoration or introduce a display face.
