# Radius

Use radius only to identify interaction behavior. Do not use radius to soften each region.

| Role | Token | Value | Eligible elements |
| --- | --- | --- | --- |
| Structural | `--rs-radius-structural` | 0 | Page regions, toolbars, tables, activity strips |
| Control | `--rs-radius-control` | 4px | Buttons, inputs, selects, compact status labels |
| Overlay | `--rs-radius-overlay` | 8px | Dialogs, popovers, menus, and floating side sheets |

Structural regions must have square corners. Do not use pill radii or raw radius values.

Do not nest rounded containers. A status label can use the control radius. Ordinary metadata must remain plain text.
