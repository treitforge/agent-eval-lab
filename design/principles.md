# RepoScout design principles

This directory is the source of truth for RepoScout's interface. The words **must**,
**must not**, **should**, and **may** are normative. When implementation and these
specifications disagree, update the implementation or make an explicit design-system
decision here; do not create a local exception by accident.

## Product model

RepoScout is an expert repository-evaluation workbench for sustained technical review. It
is not a SaaS dashboard, marketing site, landing page, or generic administration template.
It should feel precise, restrained, mature, technical, and evidence-first.

The design language combines Swiss-modernist information design, mature developer-tool
interaction patterns, and compact enterprise data-table behavior without imitating a
specific product. Use a disciplined grid, strong type alignment, deliberate asymmetry,
hairline separators, low-chroma surfaces, and one restrained green accent.

## Task hierarchy

1. **Primary:** scan, filter, sort, and compare repository candidates.
2. **Secondary:** select a candidate and inspect evidence, architecture, analysis,
   qualification state, provenance, and the acceptance or rejection rationale.
3. **Tertiary:** queue selected candidates, start discovery, and inspect operational
   activity.

The candidate list must remain the dominant visual object. Secondary and tertiary work
must not displace or visually compete with it.

## Information grammar

Group content in this order:

1. alignment;
2. proximity;
3. whitespace;
4. typographic hierarchy;
5. hairline divider;
6. subtle background change;
7. enclosed container.

Use the first method that makes a relationship clear. An enclosed container is exceptional
and requires independent behavior such as a dialog, popover, side sheet, selectable object,
or self-contained preview. The table is the page; never put it in a card.

## Interaction principles

- Keep meaningful filters, status tabs, and the selected candidate in the URL.
- Make the primary task apparent within one second.
- Use semantic HTML and established accessible primitives.
- Preserve the list when candidate detail opens.
- Make selection and focus visible without relying on color alone.
- Put uncommon row actions in an overflow menu; make the row or repository name open detail.
- Reveal batch analysis only when eligible candidates are selected.
- Use whitespace to express hierarchy, not to decorate empty space.

## Decision test

Before adding a surface, border, background, label, action, or duplicate value, ask whether
removing it harms comprehension or task completion. If it does not, remove it. A blurred or
squinted view must still read as a candidate workbench led by its table.

## Specification map

- Foundations define the only approved visual values in `src/styles/tokens.css`.
- Patterns define page-level composition and behavior.
- Components define reusable interaction contracts.
- `anti-patterns.md` defines hard visual budgets and forbidden output.
- `scripts/ui-audit.mjs` enforces the mechanically detectable subset.
