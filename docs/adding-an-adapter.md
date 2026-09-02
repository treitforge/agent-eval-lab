# Add a trajectory adapter

Use this process for a new producer format.

## 1. Find a stable source shape

Use a documented schema when one exists. Record the producer name and version. If the format has no schema version, state that limitation.

## 2. Create a synthetic fixture

Do not commit a private trajectory. Create the smallest synthetic document that contains:

- One message or step.
- One tool call.
- One explicit success or failure result.
- A timestamp or duration when the format supports it.
- A token or cost metric when the format supports it.

## 3. Normalize the facts

Add detection and conversion logic to `src/trajectory_facts/adapters.py`. Preserve the source reference. Do not execute any input content.

Use these rules:

- Read only explicit status fields.
- Use `None` when a fact is unavailable.
- Preserve tool arguments in a JSON-compatible form.
- Pair calls and results with a stable call identifier when one exists.
- Keep unpaired observations as separate events.

## 4. Add tests

Test format detection, event counts, result status, references, and metrics. Add a regression test for each producer extension that caused a parsing problem.

## 5. Update the documentation

Add the format to `docs/formats.md`. State whether it is a standard, documented vendor format, or best-effort native export.
