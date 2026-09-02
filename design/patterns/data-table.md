# Data table

## Role

The trial table is the primary work surface. It is full-width and is not in a card.

The table must support comparison and not decoration.

## Required behavior

- Use semantic table markup when the content is tabular.
- Keep headers sticky for long lists.
- Support sorting with a visible direction and `aria-sort`.
- Keep filter, sort, and page state in the URL when these functions exist.
- Support row selection without making a checkbox the only row target.
- Open the inspector from the trial row.
- Put uncommon actions in one overflow menu.

## Density and columns

Use rows that are 36–40px high. Use 12px table headers and 13–14px row text.

Use tabular numerals for time, counts, tokens, rewards, and patch sizes. Keep source references and identifiers in a monospace font.

Align text to the left. Align comparable numeric values to the right. Do not center data.

Truncate only lower-priority prose. Provide access to the full value. Use hairline row separators and a subtle selected surface.

## States

- **Selected:** use multiple cues and preserve readable status treatments.
- **Empty:** show one short table-row message. Put a recovery action outside the row when one exists.
- **Loading:** preserve column widths and table position.
- **Error:** identify the content that did not load. Provide a quiet retry action.

Do not convert rows into cards. Do not repeat an action link in each row. Do not use a pill for each metadata value.
