# Anti-patterns and visual budgets

These limits are requirements. If a design exceeds a limit, change the layout or update this contract before implementation.

## Visual budgets

| Budget | Limit |
| --- | ---: |
| Persistent surface levels | 2 |
| Generic cards in the primary view | 0 |
| Nested container depth | 0 |
| Prominent primary actions in one persistent view | 1 |
| Large filled accent regions | 1 |
| Structural shadows | 0 |
| Typography sizes per screen | Approximately 3 |
| Spacing values | 4, 8, 12, 16, 24, 32px |
| Structural radius | 0 |
| Control radius | 4px |
| Overlay radius | 8px |

## Forbidden patterns

- A row of large metric cards or a card grid as the page layout.
- A card around the trial table, a page section, metrics, or a form.
- A card around another card or a bordered panel nested inside another bordered panel.
- Structural use of a generic `Card` component. See `components/card.md` for the narrow
  exceptions.
- A large empty region when no evidence exists.
- More than one prominent primary action in the same persistent view.
- Multiple full-width solid primary buttons.
- A repeated detail action in each trial row. The row opens the inspector.
- Decorative icons beside every heading.
- Repeated tiny uppercase eyebrow headings.
- Pills for ordinary text or every metadata value.
- Large empty-state illustrations or generic hero copy above the workbench.
- Duplicate information that has no functional reason.
- `rounded-xl` or `rounded-2xl` on structural regions, raw radius values, or nested rounded
  containers.
- `shadow-*` or `box-shadow` outside a floating overlay.
- `bg-gradient-*`, CSS gradients, glassmorphism, glow, `backdrop-blur-*`, or CSS backdrop
  blur.
- Raw color values instead of semantic tokens.
- Spacing values outside the approved scale or raw spacing values instead of tokens.
- A tinted page background whose purpose is to reveal white cards.

## Review boundary

Automated tests can check only some rules. They cannot judge hierarchy, duplicate meaning, density, or the need for a surface.

A human must also review the interface against this file and `principles.md`.
