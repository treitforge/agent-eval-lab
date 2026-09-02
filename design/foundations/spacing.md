# Spacing

## Scale

Use this six-step spacing scale. Do not use an intermediate spacing value.

| Token | Value | Typical use |
| --- | --- | --- |
| `--rs-space-1` | 4px | Tight inline relationships |
| `--rs-space-2` | 8px | Control internals and compact gaps |
| `--rs-space-3` | 12px | Row cells and related controls |
| `--rs-space-4` | 16px | Section rhythm |
| `--rs-space-6` | 24px | Major region separation |
| `--rs-space-8` | 32px | Largest page-level interval |

Use `--rs-space-0` for resets. Use `auto` for layout alignment.

Use semantic size tokens for control, row, and header heights. These dimensions are not spacing values.

## Rules

- Padding, margin, gaps, and positional insets must use approved tokens.
- Do not create arbitrary spacing values to make one composition fit.
- Prefer alignment and a shared grid before increasing whitespace.
- Keep table rows approximately 36–40px and controls approximately 32–36px high.
- At 1440×900, show at least 15 trial rows when the inspector is closed.
- Preserve clear row targets and readable evidence in a compact layout.
