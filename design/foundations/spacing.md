# Spacing

## Scale

RepoScout uses a six-step 4px-based spacing scale. No intermediate values are approved.

| Token | Value | Typical use |
| --- | --- | --- |
| `--rs-space-1` | 4px | Tight inline relationships |
| `--rs-space-2` | 8px | Control internals and compact gaps |
| `--rs-space-3` | 12px | Row cells and related controls |
| `--rs-space-4` | 16px | Section rhythm |
| `--rs-space-6` | 24px | Major region separation |
| `--rs-space-8` | 32px | Largest page-level interval |

`--rs-space-0` is available for resets. `auto` is valid for layout alignment. Use semantic
size tokens for control height, table-row height, and header height; these are dimensions,
not additions to the spacing scale.

## Rules

- Padding, margin, gaps, and positional insets must use approved tokens.
- Do not create arbitrary spacing values to make one composition fit.
- Prefer alignment and a shared grid before increasing whitespace.
- Keep table rows approximately 36–40px and controls approximately 32–36px high.
- At 1440×900, the closed-inspector workbench should show at least 15 candidate rows.
- Compact does not mean cramped: preserve clear row targets and readable evidence.
