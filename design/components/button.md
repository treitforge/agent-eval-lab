# Button

## Variants

| Variant | Purpose | Budget |
| --- | --- | --- |
| Primary | Highest-priority page action | One per persistent view |
| Secondary | Standard action | Use only when necessary |
| Quiet | Toolbar, inline, or low-emphasis action | Preferred for repeated controls |
| Semantic | Retry, cancel, or another state change | Only for a state change |
| Icon | Compact familiar action with an accessible name | Avoid beside every heading |

Buttons use `--rs-radius-control` and approved spacing tokens. Use a 32px or 36px control-height token.

Use the accent color for a primary button. Do not use a second filled accent region for other buttons.

## Labeling and state

Start each label with a short verb. Examples are “Download facts,” “Open report,” and “Retry run.”

Keep the label stable while the action runs. Show progress in an accessible form.

Provide visible hover, active, disabled, and keyboard-focus states. An icon-only button must have an accessible name and a familiar icon.

## Enforcement hook

Every primary action must have `data-ui-primary="true"`. An automated test can count these actions in each persistent view.

## Do not

- Use more than one primary action in a persistent view.
- Make several solid buttons full-width in one region.
- Use primary styling for filters, refresh, navigation, or cancel.
- Rely on color alone to communicate a destructive or semantic action.
