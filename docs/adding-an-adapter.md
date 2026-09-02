# Add a trajectory adapter

Use this process to add a producer format.

## 1. Find a stable source format

Use a documented schema when one exists. Record the producer name and version. State when the format has no schema version.

## 2. Create a synthetic fixture

Do not commit a private trajectory. Create a small synthetic document that contains these items:

- One message or step.
- One tool call.
- One result with an explicit status.
- One timestamp or duration when the format supports it.
- One token or cost value when the format supports it.

## 3. Normalize the facts

Add detection and conversion logic to `src/trajectory_facts/adapters.py`. Preserve the source reference. Do not execute content from the input file.

Use these rules:

- Read only explicit status fields.
- Use `None` when a fact is not available.
- Store tool arguments in a JSON-compatible form.
- Pair a call with its result when a stable call identifier exists.
- Keep an unpaired observation as a separate event.

## 4. Add tests

Test format detection, event counts, result status, references, and metrics. Add a regression test for each parsing defect.

## 5. Update the format list

Add the format to `docs/formats.md`. Identify it as a standard, documented vendor format, or best-effort native export.
