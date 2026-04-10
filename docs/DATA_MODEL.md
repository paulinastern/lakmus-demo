# Data model: what gets tracked

This repository describes a **trial record**: one agent execution on one benchmark task, enriched with **behavioral signals** parsed from the agent trace (tool calls + assistant text).

## TrialRecord (fields)

| Field | Type | Meaning |
|-------|------|---------|
| `run_id` | str | Batch or harness run identifier |
| `trial_name` | str | Unique trial id from the harness |
| `task_name` | str | Stable task id (for regression tracking) |
| `latency_sec` | float? | Wall-clock agent execution time |
| `cost_usd` | float? | Reported API cost (if available) |
| `reward` | float? | Verifier score (e.g. 1.0 = pass) |
| `n_input_tokens` / `n_output_tokens` | int? | Token usage (major cost driver in chat-style agents) |
| `answer_file_written` | bool | Did the agent write the required output artifact? |
| `answer_file_missing` | bool | Did the verifier report missing output? |
| `written_answer` | str? | Content of the final answer (if captured) |
| `retrieval_actions` | int | Count of search/read tools (read, grep, bash used for retrieval) |
| `write_actions` | int | Count of write tool calls |
| `loop_messages` | int | Phrases suggesting continued search without progress |
| `estimate_language` | bool | Hedging / proxy language detected |
| `uncertainty_markers` | int | Count of uncertainty phrases |
| `strategy_switch_markers` | int | Count of “try something else” pivots |
| `evidence_gap_markers` | int | Count of “cannot determine from text” style phrases |
| `question_like_lines` | int | Lines with `?` (bad in non-interactive benchmarks) |
| `oversize_read_actions` | int | Reads over a configured line limit |
| `max_read_limit` | int? | Largest read limit observed |
| `repeated_read_actions` | int | Repeated identical read windows |
| `answer_rewrites` | int | How many times the final answer file was written |
| `last_reasoning_excerpt` | str? | Short tail of model text (for debugging) |
| `auth_missing` | bool | API key / auth errors in trace |
| `failure_type` | str | Coarse label (see below) |
| `trial_dir` | str | Path to artifacts (optional; redact in public dumps) |

## Failure taxonomy (example)

Labels are **heuristic** and depend on your classifier order. A typical set:

- `pass` — verifier reward ≥ threshold  
- `auth_env_missing` — missing credentials  
- `infra_error` — harness/runtime failure (reward null)  
- `termination_failure` — no required output file  
- `search_loop` — many retrievals + loop language  
- `proxy_estimation` — answer grounded in hedging / proxies  
- `wrong_answer` — output present but incorrect (often split into subtypes in production)

Subtypes like `wrong_answer:overread` or `wrong_answer:flip_flop` are optional refinements based on signals above.

## Control score

`control_score` (0–100) is a **process** summary: did the agent finalize cleanly, avoid loops, avoid oversized reads, and produce a numeric-shaped answer when it failed? It is not a substitute for task accuracy; use it to compare *how* agents behave under the same prompt.

## JSONL interchange

One JSON object per line, UTF-8. This matches common log pipelines and is easy to append after each batch.

## Privacy

Strip paths, API keys, and proprietary instruction text before publishing traces. The sample file under `examples/` is fully synthetic.
