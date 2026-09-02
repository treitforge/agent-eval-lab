# Button

## Variants

| Variant | Purpose | Budget |
| --- | --- | --- |
| Primary | Highest-priority page action | One per persistent view |
| Secondary | Ordinary explicit action | As needed, with restraint |
| Quiet | Toolbar, inline, or low-emphasis action | Preferred for repeated controls |
| Semantic | Accept, hold, reject, retry, or another actual state transition | Only when meaning is semantic |
| Icon | Compact familiar action with an accessible name | Avoid beside every heading |

Buttons use `--rs-radius-control`, approved spacing tokens, and a 32px or 36px control-height
token. Primary buttons use the accent color. Secondary and quiet buttons do not introduce a
second filled accent region.

## Labeling and state

Use short verb-led sentence-case labels: “Discover repositories,” “Queue analysis,” or “Save
note.” Keep the label stable while pending when possible and expose progress accessibly. Provide
visible hover, active, disabled, and keyboard-focus states. Icon-only buttons require an
accessible name and a familiar icon.

## Enforcement hook

Every prominent primary action must carry `data-ui-primary="true"`. The audit counts marked
interactive elements in each persistent view. Do not omit the marker to evade the budget.

## Do not

- Use more than one primary action in a persistent view.
- Make several solid buttons full-width in one region.
- Use primary styling for filters, refresh, navigation, or cancel.
- rely on color alone to communicate a destructive or semantic action.
