# Case study (high level): document QA agents on a fixed corpus

This section describes outcomes **without** tying the ideas to a specific private codebase or benchmark name.

## Problem

Teams run long-horizon agents over large text corpora. Failures are often ambiguous: wrong number, missing output, timeout, or silent “proxy” reasoning. Leaderboards show scores, not *why* a run went wrong or whether a prompt change helped or hurt the same task twice.

## Approach

Treat each evaluation as a **trial record**: verifier metrics plus behavioral signals from the trace (retrieval count, read sizes, hedging language, answer rewrites). Aggregate into:

- Failure distributions  
- Per-task histories (to spot **regressions** when a task used to pass)  
- Cost/token usage vs retrieval depth (important for chat-style agents that resend full context each turn)  

## What we observed locally (qualitative)

- **Input token volume** dominated cost more than system prompt length: repeated tool outputs accumulate in context.  
- Tightening read limits and retrieval budgets reduced cost more than micro-edits to prose.  
- A single **wrong-answer** bucket hid distinct behaviors (e.g. flip-flopping answers vs never finalizing); splitting by signals made fixes actionable.  
- **Comma formatting** and verifier preprocessing quirks could mark correct extractions as failed; the loop surfaced those faster than re-reading traces by hand.  

Replace this section with your own numbers if you publish a full write-up.

## Demo narrative (30 seconds)

“We run the agent, parse traces into a table, classify failures, and watch per-task regressions when we change prompts. The dashboard is static HTML from JSON—good for sharing without standing up infra.”
