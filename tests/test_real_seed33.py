import hashlib
import json
import os
from pathlib import Path

import pytest

from mehwar.controllers.ppo import CHECKPOINT_SHA256, MaskablePPOCheckpointAdapter
from mehwar.scenarios.c4 import C4_0000, C4_0001
from mehwar.scenarios.c4_runner import run_c4

pytestmark = pytest.mark.real_checkpoint

EXPECTED_C4_0001 = [
    (8, 9), (9, 9), (9, 10), (9, 11), (10, 12), (11, 11), (12, 10),
    (13, 9), (14, 8), (14, 7), (13, 6), (14, 5), (14, 4), (14, 3),
    (13, 2), (14, 1), (13, 0), (14, 1), (13, 0), (14, 1), (13, 0),
    (14, 1), (13, 0), (14, 1), (13, 0), (14, 1), (13, 0), (14, 1), (13, 0),
]


@pytest.fixture(scope="module")
def verified_adapter():
    checkpoint = os.environ.get("MEHWAR_SEED33_CHECKPOINT")
    if not checkpoint:
        pytest.skip("MEHWAR_SEED33_CHECKPOINT is unavailable")
    # A configured missing/corrupt file or missing dependencies must FAIL, not skip.
    path = Path(checkpoint)
    before = (path.stat().st_size, path.stat().st_mtime_ns)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == CHECKPOINT_SHA256
    adapter = MaskablePPOCheckpointAdapter(path)
    yield adapter
    assert (path.stat().st_size, path.stat().st_mtime_ns) == before
    assert hashlib.sha256(path.read_bytes()).hexdigest() == CHECKPOINT_SHA256


def test_real_checkpoint_identity_and_unique_modules(verified_adapter):
    metadata = verified_adapter.metadata()
    assert metadata["controller_family"] == "MaskablePPO"
    assert metadata["checkpoint_sha256"] == CHECKPOINT_SHA256
    assert metadata["seed"] == 33 and metadata["num_timesteps"] == 452608
    assert metadata["sb3_version"] == "2.9.0"
    assert metadata["parameter_count"] == 428937
    assert metadata["deterministic"] is True and metadata["action_masking"] is True
    assert json.loads(json.dumps(metadata)) == metadata
    policy = verified_adapter._policy
    assert sum(p.numel() for p in policy.parameters()) == 428937
    assert sum(p.numel() for p in policy.state_dict().values()) > 428937
    assert not policy.training and all(not p.requires_grad for p in policy.parameters())
    metadata["seed"] = 0
    assert verified_adapter.metadata()["seed"] == 33


@pytest.mark.parametrize(
    ("scenario", "success", "steps", "failure"),
    [(C4_0000, True, 16, "success"), (C4_0001, False, 28, "two_cell_loop")],
)
def test_real_hero_outcomes_and_repeatability(
    verified_adapter, scenario, success, steps, failure,
):
    result = run_c4(verified_adapter, scenario)
    assert result.success is success and result.steps == steps
    assert result.failure_type == failure
    assert result.diagnostics["invalid_actions"] == 0
    assert result.provenance["fresh_holdout"] is False
    assert run_c4(verified_adapter, scenario) == result
    if scenario.scenario_id == "C4-0001":
        assert result.trajectory == [list(cell) for cell in EXPECTED_C4_0001]
