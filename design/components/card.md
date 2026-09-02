# Card

Cards are exceptional objects in RepoScout, not a page-composition primitive. Prefer alignment,
proximity, whitespace, typography, dividers, or a subtle surface change.

## When to use

Use a card only when the object has an independent boundary and behavior, such as:

- an independently selectable object outside the primary candidate table;
- a self-contained preview that can move or be acted on as a unit;
- content whose object boundary is essential to understanding its interaction.

When an exception is justified, mark the component with
`data-card-purpose="selectable"` or `data-card-purpose="preview"`. Keep it flat, avoid nested
containers, and use only the structural radius unless the object is also a floating overlay.

## When not to use

Do not use a card for:

- the candidate table or candidate rows;
- page sections, headers, filters, toolbars, metrics, status counts, or forms;
- candidate evidence sections inside the inspector;
- recent jobs or empty states;
- visual decoration or a substitute for spacing and dividers;
- wrapping another card, bordered panel, or rounded container.

There are zero generic cards in the primary workbench. If several sibling regions each look
like a card, the topology is wrong even if the component has another name.
