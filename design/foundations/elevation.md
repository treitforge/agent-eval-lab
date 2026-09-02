# Elevation

Persistent interface regions are flat. Alignment, dividers, and at most two persistent
surface levels establish hierarchy.

| Token | Use |
| --- | --- |
| `--rs-shadow-none` | Every persistent or structural region |
| `--rs-shadow-overlay` | Floating dialogs, menus, popovers, and overlay side sheets only |

Do not apply shadows to headers, tables, filters, metrics, forms, panels, or other static
regions. Do not simulate elevation with gradients, glow, translucent backgrounds, or
backdrop blur. A side sheet that is docked into the list/detail grid is a persistent surface
and therefore uses no shadow; only a floating narrow-viewport variant may use overlay
elevation.
