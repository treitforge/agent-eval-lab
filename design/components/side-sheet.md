# Side sheet

## Use

Use a side sheet for a focused workflow that should preserve the workbench context:

- selected-candidate detail;
- repository discovery;
- compact operational activity.

Do not use one to hide ordinary navigation or content that belongs in the table toolbar.

## Modes

On a wide desktop, the candidate inspector is docked at roughly 30–35% of the workspace. It is
a persistent second surface with a square structural edge and no shadow. On narrower windows,
it may float as an overlay using `--rs-radius-overlay` and `--rs-shadow-overlay`.

## Behavior

- Provide a visible title and close control.
- Move focus into modal variants and trap it only when the sheet is modal.
- Return focus to the invoking action or selected row on close.
- Support Escape for an overlay variant.
- Prevent background interaction only for a modal variant.
- Keep important actions visible without stacking several full-width primary buttons.

Use alignment, headings, and dividers for internal grouping. Do not fill the sheet with nested
cards or panels.

## Audit hooks

Mark a floating sheet with `data-ui-overlay="true"` (or an equivalent dialog role) when it uses
the overlay shadow. A docked sheet must not use overlay elevation.
