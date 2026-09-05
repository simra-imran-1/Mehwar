"""Frozen C4/C5 recurrence semantics; invalid actions are separate diagnostics."""

from collections.abc import Hashable, Sequence

PROTOCOL_ID = "c4_c5_recurrence_v1"


def classify_failure(
    trajectory: Sequence[Hashable], *, success: bool, collision: bool
) -> str:
    """Classify the complete trajectory, including its initial position."""
    if success:
        return "success"
    elif collision:
        return "collision"
    elif len(trajectory) >= 4 and any(
        trajectory[i] == trajectory[i - 2] for i in range(2, len(trajectory))
    ):
        return "two_cell_loop"
    elif len(set(trajectory)) < len(trajectory):
        return "longer_loop"
    else:
        return "timeout_other"
