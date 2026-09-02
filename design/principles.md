# Interface principles

This directory is the source of truth for the Agent Eval Lab interface. The words **must** and **must not** identify requirements.

If the implementation conflicts with these rules, update the implementation or the rule. Do not create an undocumented local exception.

## Product model

Agent Eval Lab is an evidence workbench for the review of coding-agent runs. It is not a marketing site or generic administration dashboard.

The interface must be precise, restrained, technical, and evidence-first. Use a disciplined grid, aligned text, hairline separators, neutral surfaces, and one dark green accent.

## Task hierarchy

1. **Primary:** Compare the factual results of all trials.
2. **Secondary:** Select a trial and inspect its evidence, provenance, metrics, patch, and final response.
3. **Tertiary:** Download facts or open a detailed report.

The trial table must remain the main visual object. Secondary actions must not compete with the table.

## Information grammar

Group content in this order:

1. alignment;
2. proximity;
3. whitespace;
4. typographic hierarchy;
5. hairline divider;
6. subtle background change;
7. enclosed container.

Use the first method that makes a relationship clear. Use an enclosed container only for an independent object, such as a dialog or side sheet.

The table is the main surface. Do not put the table in a card.

## Interaction principles

- Make the primary task clear when the page opens.
- Use semantic HTML and accessible controls.
- Preserve the table when trial details open.
- Make selection and focus visible without color alone.
- Let a user open details from the trial row.
- Use whitespace to show hierarchy.

## Decision test

Before you add an element, confirm that the element helps comprehension or task completion. Remove an element that has no clear function.

The table must remain dominant when a user views the page from a distance.

## Specification map

- Foundations define the approved visual values in `design/tokens.css`.
- Patterns define page-level composition and behavior.
- Components define reusable interaction contracts.
- `anti-patterns.md` defines hard visual budgets and forbidden output.
- Tests must enforce rules that can be checked automatically.
