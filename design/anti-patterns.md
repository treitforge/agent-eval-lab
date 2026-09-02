# Anti-patterns and visual budgets

These limits are hard constraints. If a task appears to require exceeding one, revisit its
topology or update the design contract explicitly before implementation.

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

- A row of large KPI cards or a card grid as the page composition.
- A card around the candidate table, a page section, filters, metrics, or a form.
- A card around another card or a bordered panel nested inside another bordered panel.
- Structural use of a generic `Card` component. See `components/card.md` for the narrow
  exceptions.
- A permanently visible discovery form beside the table.
- A large empty jobs card when no activity exists.
- More than one prominent primary action in the same persistent view.
- Multiple full-width solid primary buttons.
- A repeated “Explore” action in every candidate row; selecting the row or repository name
  opens the inspector.
- Decorative icons beside every heading.
- Repeated tiny uppercase eyebrow headings.
- Pills for ordinary text or every metadata value.
- Large empty-state illustrations or generic hero copy above the workbench.
- Duplicate information in multiple regions without a functional reason.
- `rounded-xl` or `rounded-2xl` on structural regions, raw radius values, or nested rounded
  containers.
- `shadow-*` or `box-shadow` outside a floating overlay.
- `bg-gradient-*`, CSS gradients, glassmorphism, glow, `backdrop-blur-*`, or CSS backdrop
  blur.
- Raw color values or framework palette utilities instead of semantic tokens.
- Spacing values outside the approved scale or raw spacing values instead of tokens.
- A tinted page background whose purpose is to reveal white cards.

## Audit boundary

`scripts/ui-audit.mjs` checks the mechanically detectable rules in UI source. It cannot
judge information hierarchy, duplicate meaning, density, whether a surface is necessary,
or whether a card exception is honest. Human review against this file and
`principles.md` remains required.
