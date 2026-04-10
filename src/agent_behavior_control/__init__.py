"""Agent behavior control: schemas, metrics, and a tiny reporting demo.

This package is intentionally small and benchmark-agnostic. Wire your own trace
parser to populate :class:`TrialRecord` rows from your harness.
"""

from agent_behavior_control.metrics import control_score, is_numeric_answer
from agent_behavior_control.schema import TrialRecord

__all__ = ["TrialRecord", "control_score", "is_numeric_answer", "__version__"]

__version__ = "0.1.0"
