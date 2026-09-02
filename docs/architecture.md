# Architecture

Agent Eval Lab has separate stages for collection, normalization, analysis, presentation, and human evaluation.

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

`src/trajectory_facts/adapters.py` detects the source format. It converts the source document to a `RunRecord`.

Each `ToolEvent` contains available source facts. These facts include the source reference, tool name, arguments, result status, text, timestamp, and duration.

An adapter must not infer a result status from prose. It must use an explicit return code, status field, or error flag.

### Normalized records

`src/trajectory_facts/models.py` defines three record types:

- `StepRecord` contains a source message or step.
- `ToolEvent` contains a tool call and its result.
- `RunRecord` contains one normalized run.

The normalized model contains only common facts. It does not require all producers to use the same native schema.

### Analysis

`src/trajectory_facts/analyze.py` calculates deterministic facts. These facts include repeated calls, recovery groups, elapsed time, tool categories, and final-response size.

The analyzer does not assign quality, blame, severity, or preference.

### Reports

`src/trajectory_facts/render.py` creates Markdown reports. `src/trajectory_facts/cli.py` creates terminal, JSON, and Markdown output.

### Dashboard

`src/trajectory_facts/dashboard.py` reads Harbor trial directories. It combines trajectory facts with result data, verifier rewards, test output, and patch summaries.

The dashboard is a static HTML file. It does not require a server.

## Trust boundary

The analyzer treats each trajectory as untrusted input. It does not execute trajectory content. The dashboard escapes source text before it adds the text to HTML.

A report can still contain sensitive source text. Review and redact each report before you publish it.
