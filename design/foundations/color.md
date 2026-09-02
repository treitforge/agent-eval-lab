# Color

## Intent

Color supports reading and communicates a factual state. Do not use color to create decorative depth.

Use a white or near-white canvas. Use neutral gray separators and one dark green accent family.

## Approved roles

| Role | Token | Use |
| --- | --- | --- |
| Canvas | `--rs-color-canvas` | Primary page and table canvas |
| Subtle surface | `--rs-color-surface-subtle` | Hover, selection, and secondary persistent surface |
| Strong text | `--rs-color-text` | Primary content |
| Muted text | `--rs-color-text-muted` | Metadata and supporting content |
| Hairline | `--rs-color-border` | Dividers and table rules |
| Strong hairline | `--rs-color-border-strong` | Control borders and emphasized separation |
| Accent | `--rs-color-accent` | Single primary action, selected navigation, and links |
| Accent hover | `--rs-color-accent-hover` | Accent interaction state |
| Accent subtle | `--rs-color-accent-subtle` | Restrained selected state |
| Success | `--rs-color-success-*` | Successful or completed only |
| Warning | `--rs-color-warning-*` | Attention required only |
| Danger | `--rs-color-danger-*` | Failed only |
| Neutral status | `--rs-color-neutral-*` | Inactive, pending, or unknown |
| Focus | `--rs-color-focus` | Visible keyboard focus ring |

Use matching foreground and subtle-background tokens. A status must include text or an icon. Do not use color as the only status cue.

Do not fill a large region with a semantic color.

## Rules

- Use only variables from `design/tokens.css` in generated interface CSS.
- Do not use raw color values outside `design/tokens.css`.
- Use no more than one large accent region in a persistent view.
- Do not tint the page merely to make white cards visible.
- Do not use gradients, glow, translucency, or glass effects.
- Preserve text contrast in neutral hover and selected states.
- Make these states clear without color alone.
