# Data table

## Role

The candidate table is RepoScout's primary work surface. It is full-width and never enclosed
in a card. Its visual rhythm should favor comparison over decoration.

## Required behavior

- Use semantic table markup when the content is tabular.
- Keep headers sticky for long lists.
- Support sorting with a visible direction and `aria-sort`.
- Keep filter, sort, tab, and page state in the URL.
- Support row selection and multiselect without making the checkbox the only row target.
- Open the inspector from the row or repository name.
- Put uncommon actions in one overflow menu.
- Reveal contextual batch analysis only for one or more eligible selections.

## Density and columns

Target 36–40px rows. Use 12px table headers, 13–14px row content, and tabular numerals for
stars, counts, sizes, and scores. Candidate ID is monospaced. Repository name, language,
stars, status, and principal evidence should remain scannable without excessive truncation.

Align text left and comparable numeric values right. Avoid centered data. Truncate only lower
priority prose and provide access to the full value. Use hairline row separators and a subtle
neutral hover or selected surface; do not alternate decorative row colors.

## States

- **Selected:** use multiple cues and preserve readable status treatments.
- **Empty:** one concise table-row message plus the most relevant recovery action outside the
  row, if any.
- **Loading:** preserve column widths and table position.
- **Error:** state what could not load and offer a restrained retry action.

Do not convert rows into cards, repeat an action link in every row, or use a pill for every
metadata value.
