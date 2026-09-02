# Workbench layout

## Required topology

Use a desktop evaluation workbench in this order:

1. compact application header;
2. page title and one primary action;
3. status tabs with inline counts;
4. integrated search and filter toolbar;
5. full-width candidate table;
6. optional right-hand detail inspector;
7. compact activity or job status region.

The table occupies the full workspace when no inspector is open. When the inspector is open,
allocate approximately 65–70% to the table and 30–35% to detail. The split must preserve the
candidate list and its current scroll position.

## Region behavior

- Keep the application header compact and subordinate to the page task.
- Put only one persistent primary action beside the title: **Discover repositories**.
- Treat status counts as tabs or inline counters, not metrics.
- Integrate filters immediately above the table with no surrounding panel.
- Make table headers sticky within a long scrolling list.
- Show jobs in an activity strip, drawer, or dedicated activity view. Collapse the region
  when no useful activity exists.
- Launch discovery in a side sheet or focused flow; do not reserve persistent workspace for
  its form.

## Responsive behavior

The product is desktop-first. Preserve the table as long as practical. On narrower windows,
the detail inspector may become an overlay side sheet, but closing it must return focus to the
selected row. Do not translate the desktop table into a grid of candidate cards.

## Acceptance criteria

- A squinted view is dominated by the candidate table.
- At 1440×900, at least 15 rows are visible with the inspector closed.
- Secondary workflows do not compete with candidate review.
- Persistent regions use no shadow, structural radius, or unnecessary enclosure.
