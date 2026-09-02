# List/detail

## Selection model

The candidate list is the stable context; detail is an inspector, not a separate competing
page composition. Selecting a row or its repository-name control opens the inspector directly.
Do not add an “Explore” link to every row.

Keep the selected candidate in the URL so selection survives refresh and can be shared. The
selected row must use at least two cues, such as a leading marker plus a subtle surface change,
and should use `aria-current` or `aria-selected` where appropriate.

## Inspector content

Order content by reviewer need:

1. identity and qualification state;
2. decision rationale and principal evidence;
3. qualification dimensions and analysis state;
4. architecture and task affordances;
5. provenance and machine-oriented evidence;
6. review actions and notes.

Do not repeat list values unless the detail context needs them for orientation or action.
Use dividers and headings within the inspector before enclosed subcontainers.

## Keyboard and focus

- Rows or their primary controls must be keyboard reachable.
- Opening detail moves focus only when necessary; otherwise preserve list navigation.
- Closing an overlay inspector returns focus to the originating row.
- Arrow-key row navigation may be provided when implemented with an appropriate grid pattern.
- Selection, hover, and focus states must remain distinct.

## Loading and empty states

Keep the list stable while detail loads. Use concise text for missing evidence. Do not insert
an illustration, a blank card, or a second page-level spinner.
