from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterable
from pathlib import Path

from agent_behavior_control.metrics import control_score


def load_records_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def failure_distribution(records: Iterable[dict]) -> dict[str, int]:
    return dict(Counter(r.get("failure_type", "unknown") for r in records))


def task_regression_count(records: list[dict]) -> int:
    """Count pass->fail transitions per task when records are in run order."""
    by_task: dict[str, list[dict]] = {}
    for r in records:
        t = r.get("task_name") or ""
        by_task.setdefault(t, []).append(r)
    n = 0
    for trials in by_task.values():
        for i in range(1, len(trials)):
            prev = trials[i - 1]
            cur = trials[i]
            prev_pass = prev.get("reward") is not None and float(prev["reward"]) >= 1.0
            cur_pass = cur.get("reward") is not None and float(cur["reward"]) >= 1.0
            if prev_pass and not cur_pass:
                n += 1
    return n


def enrich_with_control_score(records: list[dict]) -> list[dict]:
    out: list[dict] = []
    for r in records:
        d = dict(r)
        d["control_score"] = control_score(d)
        out.append(d)
    return out


def write_minimal_html(path: Path, records: list[dict], title: str = "Behavior control demo") -> None:
    """Static single-file HTML: counts + table. No external JS/CSS hosts."""
    counts = failure_distribution(records)
    rows_html = ""
    for r in records[-30:]:
        rows_html += (
            "<tr>"
            f"<td>{_esc(r.get('task_name'))}</td>"
            f"<td>{_esc(r.get('failure_type'))}</td>"
            f"<td>{_esc(r.get('control_score'))}</td>"
            f"<td>{_esc(r.get('retrieval_actions'))}</td>"
            f"<td>{_esc(r.get('cost_usd'))}</td>"
            "</tr>"
        )
    dist_html = "".join(
        f"<div><b>{_esc(k)}</b>: {v}</div>" for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    )
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><title>{_esc(title)}</title>
<style>body{{font-family:system-ui,sans-serif;margin:24px}}table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #ccc;padding:6px 8px;font-size:14px}}th{{background:#f5f5f5}}</style>
</head><body>
<h1>{_esc(title)}</h1>
<p>Trials: {len(records)}</p>
<h2>Failure distribution</h2>{dist_html}
<h2>Recent trials</h2>
<table><thead><tr><th>Task</th><th>Failure</th><th>Control</th><th>Retrieval</th><th>Cost $</th></tr></thead>
<tbody>{rows_html}</tbody></table>
</body></html>"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")


def _esc(x: object) -> str:
    from html import escape

    if x is None:
        return "-"
    return escape(str(x), quote=True)
