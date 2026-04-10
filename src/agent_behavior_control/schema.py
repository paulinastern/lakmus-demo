from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrialRecord:
    """One evaluated agent run on a single task.

    Populated from harness outputs (reward, latency, token usage) plus
    **signals** extracted from the agent trace (tool use, language patterns).

    Field meanings are documented in ``docs/DATA_MODEL.md``.
    """

    run_id: str
    trial_name: str
    task_name: str
    latency_sec: float | None
    cost_usd: float | None
    reward: float | None
    n_input_tokens: int | None
    n_output_tokens: int | None
    answer_file_written: bool
    answer_file_missing: bool
    written_answer: str | None
    retrieval_actions: int
    write_actions: int
    loop_messages: int
    estimate_language: bool
    uncertainty_markers: int
    strategy_switch_markers: int
    evidence_gap_markers: int
    question_like_lines: int
    oversize_read_actions: int
    max_read_limit: int | None
    repeated_read_actions: int
    answer_rewrites: int
    last_reasoning_excerpt: str | None
    auth_missing: bool
    failure_type: str
    trial_dir: str

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "trial_name": self.trial_name,
            "task_name": self.task_name,
            "latency_sec": self.latency_sec,
            "cost_usd": self.cost_usd,
            "reward": self.reward,
            "n_input_tokens": self.n_input_tokens,
            "n_output_tokens": self.n_output_tokens,
            "answer_file_written": self.answer_file_written,
            "answer_file_missing": self.answer_file_missing,
            "written_answer": self.written_answer,
            "retrieval_actions": self.retrieval_actions,
            "write_actions": self.write_actions,
            "loop_messages": self.loop_messages,
            "estimate_language": self.estimate_language,
            "uncertainty_markers": self.uncertainty_markers,
            "strategy_switch_markers": self.strategy_switch_markers,
            "evidence_gap_markers": self.evidence_gap_markers,
            "question_like_lines": self.question_like_lines,
            "oversize_read_actions": self.oversize_read_actions,
            "max_read_limit": self.max_read_limit,
            "repeated_read_actions": self.repeated_read_actions,
            "answer_rewrites": self.answer_rewrites,
            "last_reasoning_excerpt": self.last_reasoning_excerpt,
            "auth_missing": self.auth_missing,
            "failure_type": self.failure_type,
            "trial_dir": self.trial_dir,
        }
