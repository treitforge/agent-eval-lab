# Color

## Intent

Color supports reading and communicates actual state. It does not create decorative depth.
The canvas is white or near-white, separators are neutral gray, and the single accent family
is dark green.

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
| Success | `--rs-color-success-*` | Accepted or completed only |
| Warning | `--rs-color-warning-*` | Held or attention-required only |
| Danger | `--rs-color-danger-*` | Rejected or failed only |
| Neutral status | `--rs-color-neutral-*` | Inactive, pending, or unknown |
| Focus | `--rs-color-focus` | Visible keyboard focus ring |

Use semantic foreground and subtle-background pairs together. Status treatments must include
text or an icon as well as color. Never fill a large region with semantic color.

## Rules

- Use only variables from `src/styles/tokens.css`; raw hex, RGB, HSL, named, or framework
  palette values are forbidden in UI source.
- Use no more than one large filled accent region in a persistent view. Ordinarily this is
  the primary action, not a page section.
- Do not tint the page merely to make white cards visible.
- Do not use gradients, glow, translucency, or glass effects.
- Neutral hover and selected states should preserve text contrast and remain distinguishable
  without color alone.
