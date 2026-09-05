import pytest

from mehwar.failure import PROTOCOL_ID, classify_failure


@pytest.mark.parametrize(
    ("trajectory", "expected"),
    [
        (["A", "B", "A"], "longer_loop"),
        (["A", "B", "A", "B"], "two_cell_loop"),
        (["A", "B", "A", "C"], "two_cell_loop"),
        (["A", "B", "C", "A"], "longer_loop"),
        (["A", "B", "C", "D"], "timeout_other"),
        ([], "timeout_other"),
    ],
)
def test_frozen_recurrence(trajectory, expected):
    assert classify_failure(trajectory, success=False, collision=False) == expected


def test_success_precedes_collision_and_recurrence():
    assert classify_failure("ABAB", success=True, collision=True) == "success"


def test_collision_precedes_recurrence():
    assert classify_failure("ABAB", success=False, collision=True) == "collision"


def test_protocol_id():
    assert PROTOCOL_ID == "c4_c5_recurrence_v1"
