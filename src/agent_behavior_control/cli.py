from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent_behavior_control.summarize import (
    enrich_with_control_score,
    failure_distribution,
    load_records_jsonl,
    task_regression_count,
    write_minimal_html,
)


def main() -> None:
    p = argparse.ArgumentParser(description="Summarize trial records JSONL and emit a tiny HTML report.")
    p.add_argument("jsonl", type=Path, help="Path to trial records JSONL (one JSON object per line)")
    p.add_argument("--html", type=Path, default=None, help="Write minimal HTML report to this path")
    args = p.parse_args()

    records = load_records_jsonl(args.jsonl)
    enriched = enrich_with_control_score(records)
    dist = failure_distribution(enriched)
    regressions = task_regression_count(enriched)

    summary = {
        "n_trials": len(enriched),
        "failure_counts": dist,
        "task_regression_transitions": regressions,
    }
    print(json.dumps(summary, indent=2))

    if args.html:
        write_minimal_html(args.html, enriched)
        print(json.dumps({"wrote_html": str(args.html.resolve())}, indent=2))


if __name__ == "__main__":
    main()
