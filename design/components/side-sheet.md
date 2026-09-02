# Side sheet

## Use

Use a side sheet for a focused workflow that must preserve the workbench context:

- selected-trial detail;
- source evidence;
- compact run activity.

Do not use a side sheet to hide normal navigation or table content.

## Modes

On a wide desktop, the trial inspector uses 30–35% of the workspace. It is a persistent surface with a square edge and no shadow.

On a narrow window, the inspector can float above the table. Use `--rs-radius-overlay` and `--rs-shadow-overlay` for this mode.

## Behavior

- Provide a visible title and close control.
- Move focus into a modal sheet. Trap focus only when the sheet is modal.
- Return focus to the invoking action or selected row on close.
- Let the Escape key close an overlay sheet.
- Prevent background interaction only for a modal variant.
- Keep important actions visible. Do not stack multiple full-width primary buttons.

Use alignment, headings, and dividers to group content. Do not put nested cards or panels in the sheet.

## Audit hooks

Mark a floating sheet with `data-ui-overlay="true"` (or an equivalent dialog role) when it uses
the overlay shadow. A docked sheet must not use overlay elevation.
