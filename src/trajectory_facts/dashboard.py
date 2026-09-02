"""Build a static, fact-only Harbor run dashboard."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .adapters import load_run
from .analyze import analyze_run
from .render import render_markdown


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected a JSON object: {path}")
    return value


def _elapsed_seconds(start: Any, finish: Any) -> float | None:
    if not isinstance(start, str) or not isinstance(finish, str):
        return None
    try:
        first = datetime.fromisoformat(start)
        last = datetime.fromisoformat(finish)
    except ValueError:
        return None
    return (last - first).total_seconds()


def _excerpt(value: str, limit: int = 4000) -> str:
    value = re.sub(
        r"(?i)\b(api[_-]?key|access[_-]?token|password|secret)(\s*[:=]\s*)\S+",
        r"\1\2[REDACTED]",
        value,
    )
    return value if len(value) <= limit else f"{value[: limit - 1]}…"


def _find_patch(trial: Path) -> Path | None:
    candidates = [
        trial / "artifacts" / "patch.diff",
        trial / "artifacts" / "logs" / "artifacts" / "patch.diff",
        trial / "patch.diff",
    ]
    return next((path for path in candidates if path.is_file()), None)


def _find_trajectory(trial: Path) -> Path | None:
    atif = trial / "agent" / "trajectory.json"
    if atif.is_file():
        return atif
    native_sessions = sorted(
        (trial / "agent" / "sessions").rglob("rollout-*.jsonl"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return native_sessions[0] if native_sessions else None


def _reward(result: dict[str, Any]) -> dict[str, Any]:
    verifier = result.get("verifier_result")
    if not isinstance(verifier, dict):
        return {}
    rewards = verifier.get("rewards")
    return dict(rewards) if isinstance(rewards, dict) else {}


def _trial_fact(trial: Path, output: Path) -> dict[str, Any]:
    trajectory_path = _find_trajectory(trial)
    if trajectory_path is None:
        raise ValueError(f"no ATIF or native Codex trajectory found under {trial}")
    result_path = trial / "result.json"
    config_path = trial / "config.json"
    result = _read_json(result_path) if result_path.is_file() else {}
    config = _read_json(config_path) if config_path.is_file() else {}
    patch_path = _find_patch(trial)
    report = analyze_run(load_run(trajectory_path), patch_path)

    agent_info = result.get("agent_info")
    agent_info = agent_info if isinstance(agent_info, dict) else {}
    model_info = agent_info.get("model_info")
    model_info = model_info if isinstance(model_info, dict) else {}
    agent_config = config.get("agent")
    agent_config = agent_config if isinstance(agent_config, dict) else {}
    agent_kwargs = agent_config.get("kwargs")
    agent_kwargs = agent_kwargs if isinstance(agent_kwargs, dict) else {}
    model = (
        model_info.get("name")
        or agent_config.get("model_name")
        or report["agent"].get("model")
        or "not available"
    )
    report["agent"].update(
        {
            "name": agent_info.get("name") or report["agent"].get("name"),
            "version": agent_info.get("version") or report["agent"].get("version"),
            "model": model,
        }
    )

    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(model)).strip("-")
    trial_output = output / "trials" / (safe_name or trial.name)
    trial_output.mkdir(parents=True, exist_ok=True)
    (trial_output / "facts.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (trial_output / "facts.md").write_text(render_markdown(report), encoding="utf-8")

    verifier_output_path = trial / "verifier" / "test-stdout.txt"
    verifier_output = (
        _excerpt(verifier_output_path.read_text(encoding="utf-8", errors="replace"))
        if verifier_output_path.is_file()
        else ""
    )
    exception = result.get("exception_info")
    exception = exception if isinstance(exception, dict) else None
    return {
        "trial_name": result.get("trial_name") or trial.name,
        "task_name": result.get("task_name"),
        "agent": report["agent"],
        "reasoning_effort": agent_kwargs.get("reasoning_effort"),
        "started_at": result.get("started_at"),
        "finished_at": result.get("finished_at"),
        "wall_elapsed_seconds": _elapsed_seconds(
            result.get("started_at"), result.get("finished_at")
        ),
        "verifier_rewards": _reward(result),
        "exception": {
            "type": exception.get("exception_type") or exception.get("type"),
            "message": _excerpt(str(exception.get("message", "")), 500),
        }
        if exception
        else None,
        "verifier_output": verifier_output,
        "facts": report,
        "fact_files": {
            "json": str((trial_output / "facts.json").relative_to(output)),
            "markdown": str((trial_output / "facts.md").relative_to(output)),
        },
    }


def collect_job_facts(job: str | Path, output: str | Path) -> dict[str, Any]:
    """Collect factual reports for each Harbor trial in one job."""

    job_path = Path(job).expanduser().resolve()
    output_path = Path(output).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    trials = sorted(
        trial
        for trial in job_path.iterdir()
        if trial.is_dir()
        and (trial / "result.json").is_file()
        and _find_trajectory(trial) is not None
    )
    if not trials:
        raise ValueError(f"no Harbor trial trajectories found under {job_path}")
    facts = [_trial_fact(trial, output_path) for trial in trials]
    return {
        "report_kind": "harbor-run-facts-v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "source_job": str(job_path),
        "job_name": job_path.name,
        "trial_count": len(facts),
        "trials": facts,
        "limits": [
            "This report contains machine-observable facts only.",
            "An explicit failed result is not automatically an agent mistake.",
            "The report does not assign ratings, severity, preference, or a winner.",
        ],
    }


def _display(value: Any) -> str:
    if value is None:
        return "not available"
    if isinstance(value, float):
        return f"{value:.3f}"
    if isinstance(value, dict):
        return ", ".join(f"{key}={item}" for key, item in value.items()) or "none"
    return str(value)


def render_comparison_markdown(data: dict[str, Any]) -> str:
    """Render a compact fact-only job summary."""

    lines = [
        "# Harbor run facts",
        "",
        "> This report contains machine-observable facts only. It does not assign ratings or a winner.",
        "",
        f"- Job: `{data['job_name']}`",
        f"- Trials: `{data['trial_count']}`",
        "",
        "| Model | Reward | Wall seconds | Steps | Tool calls | Explicit failed results | Tokens | Files changed | + / - |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for trial in data["trials"]:
        report = trial["facts"]
        counts = report["run_counts"]
        patch = report.get("patch") or {}
        lines.append(
            "| {model} | {reward} | {elapsed} | {steps} | {calls} | {failed} | "
            "{tokens} | {files} | +{adds} / -{deletes} |".format(
                model=_display(trial["agent"].get("model")),
                reward=_display(trial["verifier_rewards"]),
                elapsed=_display(trial["wall_elapsed_seconds"]),
                steps=counts["steps"],
                calls=counts["tool_calls"],
                failed=counts["explicit_failed_results"],
                tokens=report["metrics"].get("total_tokens", "not available"),
                files=patch.get("files_changed", "not available"),
                adds=patch.get("additions", "not available"),
                deletes=patch.get("deletions", "not available"),
            )
        )
    lines.extend(["", "## Limits", ""])
    lines.extend(f"- {item}" for item in data["limits"])
    return "\n".join(lines) + "\n"


def _tokens() -> str:
    repository_root = Path(__file__).resolve().parents[2]
    token_path = repository_root / "design" / "tokens.css"
    return token_path.read_text(encoding="utf-8") if token_path.is_file() else ""


def _table_rows(data: dict[str, Any]) -> str:
    rows: list[str] = []
    for index, trial in enumerate(data["trials"]):
        report = trial["facts"]
        counts = report["run_counts"]
        patch = report.get("patch") or {}
        model = html.escape(_display(trial["agent"].get("model")))
        reward = html.escape(_display(trial["verifier_rewards"]))
        rows.append(
            f'<tr tabindex="0" data-index="{index}" aria-selected="{str(index == 0).lower()}">'
            f'<td><span class="model-name">{model}</span><span class="subline">codex · '
            f"{html.escape(_display(trial.get('reasoning_effort')))}</span></td>"
            f'<td><span class="status status--neutral">{reward}</span></td>'
            f'<td class="number">{html.escape(_display(trial["wall_elapsed_seconds"]))}</td>'
            f'<td class="number">{counts["steps"]}</td>'
            f'<td class="number">{counts["tool_calls"]}</td>'
            f'<td class="number">{counts["explicit_failed_results"]}</td>'
            f'<td class="number">{html.escape(_display(report["metrics"].get("total_tokens")))}</td>'
            f'<td class="number">{html.escape(_display(patch.get("files_changed")))}</td>'
            f'<td class="number change">+{html.escape(_display(patch.get("additions")))} '
            f"/ -{html.escape(_display(patch.get('deletions')))}</td></tr>"
        )
    return "\n".join(rows)


def render_dashboard(data: dict[str, Any]) -> str:
    """Render a self-contained HTML workbench."""

    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    tokens = _tokens()
    rows = _table_rows(data)
    job_name = html.escape(str(data["job_name"]))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{job_name} · Trajectory facts</title>
  <style>
{tokens}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; min-height: 100%; background: var(--rs-color-canvas); color: var(--rs-color-text); font-family: var(--rs-font-sans); }}
body {{ font-size: var(--rs-type-body); line-height: var(--rs-leading-body); }}
button, a {{ font: inherit; }}
.shell {{ min-height: 100vh; display: grid; grid-template-rows: auto 1fr; }}
.masthead {{ min-height: 9rem; border-bottom: var(--rs-border-hairline) solid var(--rs-color-border-strong); padding: var(--rs-space-6) var(--rs-space-8); display: flex; align-items: end; justify-content: space-between; gap: var(--rs-space-8); }}
.eyebrow {{ margin: 0 0 var(--rs-space-2); color: var(--rs-color-accent); font-size: var(--rs-type-label); font-weight: var(--rs-weight-bold); letter-spacing: .11em; text-transform: uppercase; }}
h1 {{ margin: 0; font-size: var(--rs-type-page); line-height: var(--rs-leading-tight); }}
.lede {{ margin: var(--rs-space-2) 0 0; color: var(--rs-color-text-muted); max-width: 48rem; }}
.action {{ display: inline-flex; align-items: center; min-height: var(--rs-size-control); padding: 0 var(--rs-space-4); border: 1px solid var(--rs-color-accent); border-radius: var(--rs-radius-control); background: var(--rs-color-accent); color: var(--rs-color-on-accent); font-weight: var(--rs-weight-semibold); text-decoration: none; white-space: nowrap; }}
.action:hover {{ background: var(--rs-color-accent-hover); }}
.workbench {{ min-height: 0; display: grid; grid-template-columns: minmax(0, 1fr) minmax(var(--rs-size-inspector-min), 34%); }}
.main {{ min-width: 0; padding: var(--rs-space-6) var(--rs-space-8); }}
.section-heading {{ display: flex; justify-content: space-between; align-items: baseline; gap: var(--rs-space-4); margin-bottom: var(--rs-space-3); }}
.section-heading h2, .inspector h2 {{ margin: 0; font-size: var(--rs-type-body); }}
.meta {{ color: var(--rs-color-text-muted); font-size: var(--rs-type-meta); font-variant-numeric: tabular-nums; }}
.table-wrap {{ overflow: auto; border-top: 1px solid var(--rs-color-border-strong); border-bottom: 1px solid var(--rs-color-border-strong); }}
table {{ width: 100%; border-collapse: collapse; min-width: 58rem; }}
th {{ height: var(--rs-size-row-compact); padding: 0 var(--rs-space-3); background: var(--rs-color-surface-subtle); color: var(--rs-color-text-muted); font-size: var(--rs-type-label); text-align: left; font-weight: var(--rs-weight-semibold); white-space: nowrap; position: sticky; top: 0; }}
td {{ height: var(--rs-size-row); padding: var(--rs-space-2) var(--rs-space-3); border-top: 1px solid var(--rs-color-border); vertical-align: middle; }}
tbody tr {{ cursor: pointer; outline: none; }}
tbody tr:hover, tbody tr:focus {{ background: var(--rs-color-surface-subtle); }}
tbody tr[aria-selected="true"] {{ background: var(--rs-color-accent-subtle); box-shadow: inset 3px 0 0 var(--rs-color-accent); }}
.model-name {{ display: block; font-weight: var(--rs-weight-semibold); }}
.subline {{ display: block; color: var(--rs-color-text-muted); font-size: var(--rs-type-label); }}
.number {{ text-align: right; font-family: var(--rs-font-mono); font-size: var(--rs-type-meta); font-variant-numeric: tabular-nums; }}
.change {{ color: var(--rs-color-neutral-text); }}
.status {{ display: inline-flex; align-items: center; min-height: 1.5rem; padding: 0 var(--rs-space-2); border: 1px solid var(--rs-color-neutral-border); border-radius: var(--rs-radius-control); background: var(--rs-color-neutral-subtle); color: var(--rs-color-neutral-text); font-family: var(--rs-font-mono); font-size: var(--rs-type-label); white-space: nowrap; }}
.inspector {{ min-width: 0; border-left: 1px solid var(--rs-color-border-strong); background: var(--rs-color-surface-subtle); overflow: auto; padding: var(--rs-space-6); }}
.inspector-head {{ padding-bottom: var(--rs-space-4); border-bottom: 1px solid var(--rs-color-border-strong); }}
.inspector-model {{ margin: var(--rs-space-1) 0 0; font-size: var(--rs-type-page-compact); line-height: var(--rs-leading-tight); }}
.fact-section {{ padding: var(--rs-space-4) 0; border-bottom: 1px solid var(--rs-color-border); }}
.fact-section h3 {{ margin: 0 0 var(--rs-space-3); color: var(--rs-color-text-muted); font-size: var(--rs-type-label); letter-spacing: .08em; text-transform: uppercase; }}
.facts {{ margin: 0; display: grid; grid-template-columns: minmax(7rem, 1fr) auto; gap: var(--rs-space-2) var(--rs-space-4); }}
.facts dt {{ color: var(--rs-color-text-muted); }}
.facts dd {{ margin: 0; font-family: var(--rs-font-mono); font-size: var(--rs-type-meta); text-align: right; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }}
.event-list {{ list-style: none; margin: 0; padding: 0; display: grid; gap: var(--rs-space-3); }}
.event-list li {{ padding-left: var(--rs-space-3); border-left: 2px solid var(--rs-color-neutral-border); }}
.event-ref {{ display: block; font-family: var(--rs-font-mono); font-size: var(--rs-type-label); color: var(--rs-color-text-muted); }}
.event-text {{ display: block; margin-top: var(--rs-space-1); overflow-wrap: anywhere; }}
.empty {{ color: var(--rs-color-text-muted); }}
.limits {{ margin: var(--rs-space-6) 0 0; color: var(--rs-color-text-muted); font-size: var(--rs-type-meta); }}
:focus-visible {{ box-shadow: var(--rs-focus-ring); }}
@media (max-width: 900px) {{ .masthead {{ align-items: start; flex-direction: column; padding: var(--rs-space-6); }} .workbench {{ grid-template-columns: 1fr; }} .main {{ padding: var(--rs-space-6); }} .inspector {{ border-left: 0; border-top: 1px solid var(--rs-color-border-strong); }} }}
  </style>
</head>
<body>
<div class="shell">
  <header class="masthead">
    <div>
      <p class="eyebrow">Agent Eval Lab / Harbor run</p>
      <h1>Trajectory facts</h1>
      <p class="lede">Machine-observable run evidence for <span class="meta">{job_name}</span>. No ratings, severity labels, preference, or winner selection.</p>
    </div>
    <a class="action" href="comparison.json" download>Download facts</a>
  </header>
  <div class="workbench">
    <main class="main">
      <div class="section-heading"><h2>Trial comparison</h2><span class="meta">{data["trial_count"]} trials · select a row for details</span></div>
      <div class="table-wrap">
        <table aria-label="Trial fact comparison">
          <thead><tr><th>Model</th><th>Verifier reward</th><th class="number">Wall seconds</th><th class="number">Steps</th><th class="number">Tool calls</th><th class="number">Explicit failures</th><th class="number">Tokens</th><th class="number">Files</th><th class="number">Lines + / -</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <p class="limits">An explicit failed result is a recorded command or tool outcome. It is not automatically an agent mistake.</p>
    </main>
    <aside class="inspector" aria-live="polite">
      <div class="inspector-head"><span class="eyebrow">Selected trial</span><h2 class="inspector-model" id="model">—</h2><div class="meta" id="trial-meta">—</div></div>
      <div id="details"></div>
    </aside>
  </div>
</div>
<script id="run-data" type="application/json">{payload}</script>
<script>
const run = JSON.parse(document.getElementById('run-data').textContent);
const rows = Array.from(document.querySelectorAll('tbody tr'));
const text = value => value === null || value === undefined ? 'not available' : (typeof value === 'object' ? (Object.entries(value).map(([k,v]) => `${{k}}=${{v}}`).join(', ') || 'none') : String(value));
const esc = value => text(value).replace(/[&<>"']/g, char => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[char]));
const factRows = entries => `<dl class="facts">${{entries.map(([key,value]) => `<dt>${{esc(key)}}</dt><dd>${{esc(value)}}</dd>`).join('')}}</dl>`;
function selectTrial(index) {{
  rows.forEach((row, rowIndex) => row.setAttribute('aria-selected', String(rowIndex === index)));
  const trial = run.trials[index];
  const facts = trial.facts;
  const counts = facts.run_counts;
  const patch = facts.patch || {{}};
  document.getElementById('model').textContent = text(trial.agent.model);
  document.getElementById('trial-meta').textContent = `${{text(trial.agent.name)}} · ${{text(trial.reasoning_effort)}} reasoning`;
  const failures = facts.failed_results.length
    ? `<ul class="event-list">${{facts.failed_results.map(item => `<li><span class="event-ref">${{esc(item.reference)}} · rc=${{esc(item.return_code)}}</span><span class="event-text">${{esc(item.result_excerpt)}}</span></li>`).join('')}}</ul>`
    : '<p class="empty">No explicit failed result was present.</p>';
  const files = patch.files && patch.files.length ? patch.files.join(', ') : 'not available';
  document.getElementById('details').innerHTML = `
    <section class="fact-section"><h3>Outcome</h3>${{factRows([
      ['Verifier reward', trial.verifier_rewards], ['Started', trial.started_at], ['Finished', trial.finished_at], ['Wall seconds', trial.wall_elapsed_seconds], ['Exception', trial.exception ? `${{trial.exception.type}}: ${{trial.exception.message}}` : 'none']
    ])}}</section>
    <section class="fact-section"><h3>Agentic workflow evidence</h3>${{factRows([
      ['Steps', counts.steps], ['Tool calls', counts.tool_calls], ['Explicit successes', counts.explicit_success_results], ['Explicit failures', counts.explicit_failed_results], ['Failure signatures', counts.unique_failure_signatures], ['Repeated-call groups', counts.exact_repeated_call_groups], ['Failure→success groups', counts.failure_then_success_same_call_groups]
    ])}}</section>
    <section class="fact-section"><h3>Token evidence</h3>${{factRows([
      ['Input tokens', facts.metrics.input_tokens], ['Cached input tokens', facts.metrics.cached_input_tokens], ['Output tokens', facts.metrics.output_tokens], ['Reasoning output tokens', facts.metrics.reasoning_output_tokens], ['Total tokens', facts.metrics.total_tokens], ['Model context window', facts.metrics.model_context_window]
    ])}}</section>
    <section class="fact-section"><h3>Core functionality evidence</h3>${{factRows([
      ['Test/build events', facts.axis_evidence.core_functionality.test_and_build_events.length], ['Verifier output', trial.verifier_output || 'not available']
    ])}}</section>
    <section class="fact-section"><h3>Patch structure</h3>${{factRows([
      ['Files changed', patch.files_changed], ['Additions', patch.additions], ['Deletions', patch.deletions], ['Hunks', patch.hunks], ['Files', files]
    ])}}</section>
    <section class="fact-section"><h3>Codebase context evidence</h3>${{factRows([
      ['Read/search/inspection events', facts.axis_evidence.effective_use_of_codebase_context.read_search_and_inspection_events.length], ['Style-tool events', facts.axis_evidence.coding_style.style_tool_events.length], ['Benchmark events', facts.axis_evidence.code_efficiency.benchmark_events.length]
    ])}}</section>
    <section class="fact-section"><h3>Explicit failed results</h3>${{failures}}</section>
    <section class="fact-section"><h3>Final response facts</h3>${{factRows([
      ['Present', facts.axis_evidence.final_response_presentation.present], ['Characters', facts.axis_evidence.final_response_presentation.character_count], ['Lines', facts.axis_evidence.final_response_presentation.line_count], ['Reference', facts.axis_evidence.final_response_presentation.reference]
    ])}}</section>`;
}}
rows.forEach((row, index) => {{ row.addEventListener('click', () => selectTrial(index)); row.addEventListener('keydown', event => {{ if (event.key === 'Enter' || event.key === ' ') {{ event.preventDefault(); selectTrial(index); }} }}); }});
selectTrial(0);
</script>
</body>
</html>
"""


def build_dashboard(job: str | Path, output: str | Path) -> Path:
    """Write JSON, Markdown, and HTML run facts."""

    output_path = Path(output).expanduser().resolve()
    data = collect_job_facts(job, output_path)
    (output_path / "comparison.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output_path / "comparison.md").write_text(
        render_comparison_markdown(data), encoding="utf-8"
    )
    dashboard_path = output_path / "index.html"
    dashboard_path.write_text(render_dashboard(data), encoding="utf-8")
    return dashboard_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a fact-only dashboard for a local Harbor job."
    )
    parser.add_argument("--job", required=True, help="Harbor job directory")
    parser.add_argument("--output", required=True, help="Output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        path = build_dashboard(args.job, args.output)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"trajectory-dashboard: {error}")
        return 2
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
