# Card

Cards are exceptional objects. Do not use cards as the basic page layout.

Use alignment, proximity, whitespace, typography, dividers, or a subtle surface change first.

## When to use

Use a card only when the object has an independent boundary and behavior, such as:

- an independently selectable object outside the primary trial table;
- a self-contained preview that can move or be acted on as a unit;
- content whose object boundary is essential to understanding its interaction.

When a card is necessary, mark it with `data-card-purpose="selectable"` or `data-card-purpose="preview"`.

Keep the card flat. Do not put another container in the card. Use overlay radius only when the card is a floating overlay.

## When not to use

Do not use a card for:

- the trial table or trial rows;
- page sections, headers, filters, toolbars, metrics, status counts, or forms;
- evidence sections inside the inspector;
- recent jobs or empty states;
- visual decoration or a substitute for spacing and dividers;
- wrapping another card, bordered panel, or rounded container.

The primary workbench has no generic cards. If adjacent regions look like cards, change the page layout.
