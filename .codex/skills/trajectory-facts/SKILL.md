---
name: trajectory-facts
description: Extract machine-observable facts from agent trajectory JSON, JSONL, ATIF, OTLP, SWE-agent, Mini-SWE-Agent, and common native chat exports. Use it to count steps, failed results, exact repeats, recoveries, time, tokens, tool use, and patch structure, or to group factual evidence under evaluation axes. Do not use it to assign ratings, select a winner, or write evaluation prose for the human.
---

# Trajectory Facts

Use the repository analyzer before you make claims about a run:

```powershell
python .codex/skills/trajectory-facts/scripts/analyze.py <trajectory-path>
```

Add `--patch <patch-path>` when a unified diff is available. Use `--json-output` when another tool must consume the facts.

## Evidence contract

- Cite the source step or event for each specific fact.
- Count a failed result only when the source has an explicit nonzero return code, error status, or error flag.
- Keep raw failed-result counts separate from agent mistakes. A failed result can be an intentional reproduction or a harness result.
- Use `exact repeat` only for the same tool and the same arguments.
- Report missing timestamps, statuses, or metrics as unavailable.
- Do not infer private reasoning that the trajectory does not record.
- Keep excerpts short and redact credentials.

## Human-authorship boundary

Do not write or rewrite the final evaluation prompt, rating, preference, failure-mode selection, or submission explanation. Do not select a winning model. Give the human the source facts and check the factual accuracy of text that the human writes.

Read [references/evidence-taxonomy.md](references/evidence-taxonomy.md) when the user asks to group facts by evaluation axis or capability area. Read [references/formats.md](references/formats.md) when format detection fails or the user asks about schema support.

Verify important claims in the source trajectory after the analyzer runs. The analyzer is deterministic, but a tool-native export can omit fields or use a new vendor extension.
