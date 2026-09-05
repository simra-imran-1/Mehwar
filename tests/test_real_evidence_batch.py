import os

import pytest

from mehwar.dashboard.local_demo import run_selected_c4_batch
from mehwar.evidence import FAILURE_BOUNDARY_OBSERVED, build_evidence_profile

pytestmark = pytest.mark.real_checkpoint


def test_real_selected_batch_has_current_raw_evidence_profile():
    if not os.environ.get("MEHWAR_SEED33_CHECKPOINT"):
        pytest.skip("MEHWAR_SEED33_CHECKPOINT is unavailable")

    results = run_selected_c4_batch()
    profile = build_evidence_profile(results)

    assert profile.scenario_ids == ("C4-0000", "C4-0001")
    assert profile.scenarios_evaluated == 2
    assert profile.mission_completions == 1
    assert profile.mission_failures == 1
    assert profile.failure_type_counts == {"success": 1, "two_cell_loop": 1}
    assert profile.invalid_actions_complete is True
    assert profile.invalid_actions_total == 0
    assert profile.reference_results_available == 2
    assert profile.reference_completions == 2
    assert profile.evidence_label == FAILURE_BOUNDARY_OBSERVED
    assert all(result.provenance["fresh_holdout"] is False for result in results)
