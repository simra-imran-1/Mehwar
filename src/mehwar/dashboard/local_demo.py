"""Local selected-demo input with inference dependencies loaded only on request."""

import os

from mehwar.contracts import EvaluationResult
from mehwar.dashboard.data import DashboardDataError

CHECKPOINT_ENV = "MEHWAR_SEED33_CHECKPOINT"


def checkpoint_path_from_environment() -> str:
    checkpoint = os.environ.get(CHECKPOINT_ENV, "").strip()
    if not checkpoint:
        raise DashboardDataError(
            f"Set {CHECKPOINT_ENV} to the verified seed-33 checkpoint path, "
            "then restart Streamlit. No demo was run."
        )
    return checkpoint


def run_local_c4_demo(scenario_id: str) -> EvaluationResult:
    """Execute one verified controller/scenario through the common T4 evaluator."""
    checkpoint = checkpoint_path_from_environment()
    from mehwar.scenarios.c4 import C4_SCENARIOS

    if scenario_id not in C4_SCENARIOS:
        raise DashboardDataError("Choose C4-0000 or C4-0001 for the selected demo.")
    try:
        from mehwar.controllers.ppo import MaskablePPOCheckpointAdapter
        from mehwar.scenarios.c4_runner import run_c4

        controller = MaskablePPOCheckpointAdapter(checkpoint)
        return run_c4(controller, C4_SCENARIOS[scenario_id])
    except ImportError as exc:
        raise DashboardDataError(
            'Local inference requires the ppo extra: pip install -e ".[ppo,dashboard]"'
        ) from exc
    except (OSError, ValueError, RuntimeError) as exc:
        raise DashboardDataError(f"Verified C4 demo could not run: {exc}") from exc
