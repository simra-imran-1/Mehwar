"""Local selected-demo input with inference dependencies loaded only on request."""

import os

from mehwar.contracts import EvaluationResult
from mehwar.dashboard.data import DashboardDataError

CHECKPOINT_ENV = "MEHWAR_SEED33_CHECKPOINT"
SELECTED_DEMO_SCENARIO_IDS = ("C4-0000", "C4-0001")
_SAFE_CHECKPOINT_ERROR_DETAILS = (
    "Checkpoint SHA256 does not match frozen seed-33 model",
    "Checkpoint is missing required SB3 ZIP members",
    "Invalid SB3 checkpoint archive metadata",
    "Checkpoint seed must be 33",
    "Checkpoint num_timesteps must be 452608",
    "Checkpoint SB3 version must be 2.9.0",
    "Checkpoint feature aliases disagree",
    "Unique policy parameter count must be 428937",
)


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
        raise DashboardDataError(
            _safe_execution_error("Verified C4 demo", exc)
        ) from exc


def run_selected_c4_batch() -> tuple[EvaluationResult, ...]:
    """Execute the selected MVP demo set through the existing C4/T4 path."""
    checkpoint = checkpoint_path_from_environment()
    try:
        from mehwar.controllers.ppo import MaskablePPOCheckpointAdapter
        from mehwar.scenarios.c4 import C4_SCENARIOS
        from mehwar.scenarios.c4_runner import run_c4

        controller = MaskablePPOCheckpointAdapter(checkpoint)
        return tuple(
            run_c4(controller, C4_SCENARIOS[scenario_id])
            for scenario_id in SELECTED_DEMO_SCENARIO_IDS
        )
    except ImportError as exc:
        raise DashboardDataError(
            'Local inference requires the ppo extra: pip install -e ".[ppo,dashboard]"'
        ) from exc
    except (OSError, ValueError, RuntimeError) as exc:
        raise DashboardDataError(
            _safe_execution_error("Selected C4 demo batch", exc)
        ) from exc


def _safe_execution_error(operation: str, error: Exception) -> str:
    message = str(error)
    safe_detail = next(
        (detail for detail in _SAFE_CHECKPOINT_ERROR_DETAILS if detail in message),
        None,
    )
    if safe_detail is not None:
        return f"{operation} could not run: {safe_detail}"
    return (
        f"{operation} could not run. Verify the configured checkpoint and runtime; "
        "local filesystem paths are not displayed."
    )
