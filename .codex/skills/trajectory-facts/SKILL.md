---
name: trajectory-facts
description: Extract observable facts from agent trajectories. Count events, results, repeats, recoveries, time, tokens, tool use, and patch structure. Do not assign ratings or select a winner.
---

# Trajectory Facts

Run the repository analyzer before you make a claim about a run:

```powershell
python .codex/skills/trajectory-facts/scripts/analyze.py <trajectory-path>
```

If a unified diff is available, add `--patch <patch-path>`. Use `--json-output` when another tool reads the facts.

## Output requirements

- Write short and direct sentences.
- Use active voice and present tense.
- Use the same term for the same item.
- Give one instruction in each sentence.
- Use `must` for a requirement.
- Use `can` for a capability.
- Use `do not` for a prohibition.
- Do not use idioms, slang, contractions, or decorative language.
- Keep each excerpt short.

## Evidence contract

- Cite the source step or event for each fact.
- Count a failed result only when the source has an explicit nonzero return code, error status, or error flag.
- Keep failed-result counts separate from agent mistakes. A failed result can be an intentional reproduction or a harness result.
- Use `exact repeat` only for the same tool and the same arguments.
- Report missing timestamps, statuses, or metrics as unavailable.
- Do not infer reasoning that the trajectory does not record.
- Keep excerpts short and redact credentials.

## Human-authorship boundary

Do not write or revise an evaluation prompt, rating, preference, failure-mode selection, or submission explanation. Do not select a winning model.

Give the human the source facts. Check a human claim against the cited event.

Read [references/evidence-taxonomy.md](references/evidence-taxonomy.md) when the user requests facts by evaluation axis or capability area.

Read [references/formats.md](references/formats.md) when format detection fails. Also read it when the user asks about schema support.

After the analyzer runs, verify important claims in the source trajectory. A native export can omit fields or use a new extension.
