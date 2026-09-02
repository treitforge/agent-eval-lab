# Architecture

Agent Eval Lab separates collection, normalization, analysis, presentation, and human evaluation.

## Data flow

```text
producer export
      |
      v
format adapter ----> normalized RunRecord
                            |
                            v
                    deterministic analysis
                            |
                +-----------+-----------+
                |                       |
                v                       v
          JSON/Markdown            HTML dashboard
                |                       |
                +-----------+-----------+
                            |
                            v
                     human evaluation
```

## Components

### Adapters

`src/trajectory_facts/adapters.py` detects the input shape. It converts the source document to a `RunRecord`. Each `ToolEvent` keeps a source reference, tool name, arguments, explicit result status, result text, timestamp, and duration when those fields exist.

An adapter must not guess that prose such as `failed to reproduce` is a failed tool result. It must use a nonzero return code, an error status, or an error flag.

### Normalized records

`src/trajectory_facts/models.py` defines three data types:

- `StepRecord` holds a source message or step.
- `ToolEvent` holds a tool call and its result.
- `RunRecord` holds one normalized run.

The normalized model is intentionally small. It preserves common facts without claiming that all producers have the same native schema.

### Analysis

`src/trajectory_facts/analyze.py` computes deterministic facts. Examples include exact repeated calls, failure-then-success groups, elapsed time, tool categories, and final-response size.

The analyzer does not assign quality, blame, severity, or preference.

### Reports

`src/trajectory_facts/render.py` writes Markdown. `src/trajectory_facts/cli.py` writes terminal, JSON, and Markdown output.

### Dashboard

`src/trajectory_facts/dashboard.py` reads Harbor trial directories. It joins trajectory facts with result metadata, verifier rewards, test output, and patch summaries. It creates a static workbench with no server dependency.

## Trust boundary

The analyzer treats trajectories as untrusted input. It does not execute trajectory content. The generated HTML escapes inserted text. The tool can still copy sensitive source text into a report. Review a report before you publish it.
