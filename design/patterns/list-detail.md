# List/detail

## Selection model

The trial list is the stable context. Trial detail is an inspector and not a separate page.

Selecting a trial row opens the inspector. Do not add a separate detail link to each row.

Keep the selected trial in the URL when the dashboard supports shareable state. Use at least two cues to identify the selected row.

Use `aria-current` or `aria-selected` when it is appropriate.

## Inspector content

Order content by reviewer need:

1. agent, model, and verifier outcome;
2. run time, status, and exception data;
3. agent-process facts;
4. token and core-functionality facts;
5. patch and codebase-context facts;
6. failed results and final-response facts.

Do not repeat table values unless the inspector needs them for context. Use headings and dividers before you add an enclosed container.

## Keyboard and focus

- Trial rows or their primary controls must be keyboard accessible.
- Opening detail moves focus only when necessary; otherwise preserve list navigation.
- Closing an overlay inspector returns focus to the originating row.
- You can add arrow-key navigation when the table uses an appropriate grid pattern.
- Selection, hover, and focus states must remain distinct.

## Loading and empty states

Keep the trial list stable while details load. Use short text for missing evidence.

Do not add an illustration, blank card, or second page-level spinner.
