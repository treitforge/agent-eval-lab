# Radius

RepoScout uses radius to describe interaction behavior, never to soften every region.

| Role | Token | Value | Eligible elements |
| --- | --- | --- | --- |
| Structural | `--rs-radius-structural` | 0 | Page regions, toolbars, tables, activity strips |
| Control | `--rs-radius-control` | 4px | Buttons, inputs, selects, compact status labels |
| Overlay | `--rs-radius-overlay` | 8px | Dialogs, popovers, menus, and floating side sheets |

Structural regions must have square corners. Do not use `rounded-xl`, `rounded-2xl`, pill
radii, or raw radius values. Nested rounded containers are forbidden. A status label may use
the control radius; ordinary metadata must remain plain text.
