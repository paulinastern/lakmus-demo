from __future__ import annotations


def is_numeric_answer(ans: object) -> bool:
    """Heuristic: final answer looks like a number or comma-separated numeric list."""
    if not isinstance(ans, str):
        return False
    s = ans.strip()
    if not s:
        return False
    allowed = set("0123456789-+.,[] ")
    return all(ch in allowed for ch in s)


def control_score(row: dict) -> float:
    """Single scalar summarizing *process* quality (not correctness).

    Penalizes missing outputs, hedging language, oversized reads, loops, and
    non-numeric answers on failures. Tweak weights for your benchmark.

    ``row`` may be a :class:`dict` or anything supporting ``.get`` like a
    :class:`agent_behavior_control.schema.TrialRecord` converted via
    :meth:`TrialRecord.to_dict`.
    """
    score = 100.0
    if not bool(row.get("answer_file_written")):
        score -= 30.0
    if bool(row.get("answer_file_missing")):
        score -= 20.0
    if int(row.get("question_like_lines") or 0) > 0:
        score -= 10.0
    if bool(row.get("estimate_language")):
        score -= 12.0
    if int(row.get("oversize_read_actions") or 0) > 0:
        score -= 12.0
    if int(row.get("repeated_read_actions") or 0) >= 2:
        score -= 8.0
    if int(row.get("retrieval_actions") or 0) > 10:
        score -= 8.0
    ft = row.get("failure_type", "")
    if ft != "pass" and not is_numeric_answer(row.get("written_answer")):
        score -= 10.0
    if ft == "pass":
        score += 8.0
    return round(max(0.0, min(100.0, score)), 1)
