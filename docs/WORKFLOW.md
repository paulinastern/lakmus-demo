# Workflow: the behavior control loop

This document is **harness-agnostic**. It describes the loop that worked well in practice for long-horizon document QA agents.

## 1. Run

Execute the benchmark (or a smoke subset). Persist per-trial artifacts: verifier output, reward, latency, token usage, and a **structured agent trace** (tool calls + model text).

## 2. Ingest

For each trial directory (or log stream), parse the trace into a flat **signal vector** (counts and booleans) and merge harness metrics into a `TrialRecord` row.

## 3. Classify

Assign `failure_type` using an ordered rule list, for example: auth → infra → missing output → pass → search loop → estimation → wrong answer. Keep the order explicit so results are reproducible.

## 4. Aggregate

- Failure distribution across all trials  
- Per-task timelines (for regression: pass → fail on the same `task_name`)  
- Cost and **input tokens vs retrieval_actions** (chat agents often scale super-linearly with context)  
- Optional: “control score” trend over time  

## 5. Recommend

Map dominant failure types to **one small change** at a time (prompt rule, instruction hint, or harness limit). Avoid bundling five fixes; you will not know what worked.

## 6. (Optional) Patch

If you own the prompt file, apply a single append or replace, log the diff, rerun smoke, compare pass rate and average cost.

## 7. Report

Emit machine-readable summaries (JSON/JSONL) and a **static HTML** dashboard for demos. No server required if you embed serialized data in the page.

## What this repo includes

- The **data model** and **metrics** (`src/agent_behavior_control/`)  
- A **minimal CLI** that reads JSONL and prints summary JSON + optional HTML  
- Documentation you can share publicly  

## What you implement yourself

- Trace parser for your agent stack  
- Rich dashboard, regression diff engine, or auto-patch runner (if you want them and they are not part of your private product)
