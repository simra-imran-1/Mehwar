"""Frozen global_local observations and selected C4 episode execution."""

from __future__ import annotations

from collections.abc import Mapping
from numbers import Integral

from mehwar import evaluator
from mehwar.contracts import Controller, EvaluationResult, JsonValue
from mehwar.evaluator import ExecutionRecord
from mehwar.failure import PROTOCOL_ID, classify_failure
from mehwar.references.astar import astar
from mehwar.scenarios.c4 import (
    C4_SCENARIOS,
    MOVEMENT_CONTRACT,
    C4Scenario,
    Position,
    destination,
    legal_actions,
    movement_cost,
)


def build_observation(
    scenario: C4Scenario, position: Position, previous_action: int | None = None,
) -> dict[str, object]:
    """Build float32 maps. Channels 1, 2, 5 and 7 remain zero in static C4."""
    import numpy as np

    local = np.zeros((8, 11, 11), dtype=np.float32)
    global_map = np.zeros((8, 32, 32), dtype=np.float32)
    size = scenario.grid_size
    for row in range(size):
        for col in range(size):
            cell = (row, col)
            br, bc = min(31, row * 32 // size), min(31, col * 32 // size)
            channel = 0 if cell in scenario.blocked else 6
            global_map[channel, br, bc] = 1
    for channel, cell in ((3, position), (4, scenario.goal)):
        br, bc = (min(31, index * 32 // size) for index in cell)
        global_map[channel, br, bc] = 1
    for lr in range(11):
        for lc in range(11):
            cell = (position[0] + lr - 5, position[1] + lc - 5)
            if not all(0 <= index < size for index in cell):
                local[0, lr, lc] = 1
                continue
            channel = 0 if cell in scenario.blocked else 6
            local[channel, lr, lc] = 1
            if cell == position:
                local[3, lr, lc] = 1
            if cell == scenario.goal:
                local[4, lr, lc] = 1
    scalars = np.array([
        (scenario.goal[0] - position[0]) / (size - 1),
        (scenario.goal[1] - position[1]) / (size - 1),
        size / 100.0,
        -1.0 if previous_action is None else float(previous_action),
    ], dtype=np.float32)
    return {"local_map": local, "global_map": global_map, "scalars": scalars}


def _execute_c4(
    controller: Controller[Mapping[str, object], int], scenario: C4Scenario,
) -> ExecutionRecord:
    """Run one episode; steps counts completed moves, including repeated cells.

    Illegal actions end the episode without movement or cost. Attempt counts are
    recorded separately. Recurrence is classified after termination, never used
    as an early-stop condition. The common evaluator owns controller reset;
    this raw execution function never resets the controller.
    """
    position = scenario.start
    trajectory = [position]
    previous_action = None
    path_cost = 0.0
    invalid_actions = 0
    attempted_actions = 0
    collision = False
    success = position == scenario.goal
    while not success and len(trajectory) - 1 < scenario.episode_budget:
        allowed = legal_actions(scenario, position)
        observation = build_observation(scenario, position, previous_action)
        action = controller.act(observation, allowed)
        attempted_actions += 1
        if isinstance(action, bool) or not isinstance(action, Integral) or (
            action not in allowed
        ):
            invalid_actions += 1
            collision = True
            break
        action = int(action)
        position = destination(position, action)
        trajectory.append(position)
        path_cost += movement_cost(action)
        previous_action = action
        success = position == scenario.goal
    return ExecutionRecord(
        success=success,
        steps=len(trajectory) - 1,
        path_cost=path_cost,
        failure_type=classify_failure(trajectory, success=success, collision=collision),
        trajectory=[list(cell) for cell in trajectory],
        diagnostics={
            "invalid_actions": invalid_actions, "collision": collision,
            "attempted_actions": attempted_actions,
            "truncated": not success and not collision,
        },
    )


def run_c4(
    controller: Controller[Mapping[str, object], int], scenario: C4Scenario,
) -> EvaluationResult:
    """Evaluate a C4 episode through T4, which owns the single pre-run reset."""
    reference = astar(scenario)
    selected_demo = C4_SCENARIOS.get(scenario.scenario_id) == scenario
    provenance: dict[str, JsonValue] = {
        "measurement_source": "current MEHWAR C4 runner execution",
        "scenario_source": (
            "frozen C4 development-validation manifest excerpt"
            if selected_demo else "caller-supplied scenario; source not verified"
        ),
        "scenario_selection": (
            "selected current MVP demo" if selected_demo else "custom scenario"
        ),
        "fresh_holdout": False,
        "failure_protocol": PROTOCOL_ID,
        "movement_contract": (
            "8-connected destination-cell-only, corner cutting allowed, "
            "orthogonal cost 1, diagonal cost sqrt(2)"
        ),
        "controller_metadata_source": "controller.metadata()",
    }
    if selected_demo:
        provenance.update({
            "data_classification": "current-mehwar-selected-demo-run",
            "research_source_repository": "muzzammilsajid1/uav-dynamic-routing",
            "research_source_commit": "95b8ec3834e79464e18dd9cdcef3c0378ba343cc",
            "scenario_manifest": "evaluation/manifests/rl_v3_phase_c4_validation.json",
            "scenario_manifest_git_blob": "d687a62a72dc266eb9092fa36221cba7fe309153",
            "scenario_classification": "development_validation",
        })
    return evaluator.evaluate(
        controller_id=type(controller).__name__,
        controller=controller,
        scenario_id=scenario.scenario_id,
        scenario_family=scenario.family,
        scenario_runner=lambda active_controller: _execute_c4(
            active_controller, scenario,
        ),
        reference_result={
            "planner": "A*", "found": reference.found, "steps": reference.steps,
            "cost": reference.cost,
            "trajectory": [list(cell) for cell in reference.trajectory],
            "movement_contract": MOVEMENT_CONTRACT,
        },
        configuration={
            "grid_size": scenario.grid_size, "difficulty": scenario.difficulty,
            "start": list(scenario.start), "goal": list(scenario.goal),
            "blocked": [list(cell) for cell in sorted(scenario.blocked)],
            "episode_budget": scenario.episode_budget,
            "budget_rule": "max(10, ceil(optimal_steps * 2.0))",
            "manifest_optimal_steps": scenario.optimal_steps,
            "manifest_optimal_cost": scenario.optimal_cost,
            "movement_contract": MOVEMENT_CONTRACT,
            "observation_protocol": "C4 frozen global_local; recency channel zero",
            "failure_protocol": PROTOCOL_ID,
            "step_definition": "completed legal moves",
            "dynamics": False,
        },
        provenance=provenance,
    )


def main() -> None:
    import argparse

    from mehwar.controllers.ppo import MaskablePPOCheckpointAdapter
    from mehwar.reporting import render_human_report, result_to_json
    from mehwar.scenarios.c4 import C4_SCENARIOS

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--scenario", choices=C4_SCENARIOS, default="C4-0001")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    controller = MaskablePPOCheckpointAdapter(args.checkpoint)
    result = run_c4(controller, C4_SCENARIOS[args.scenario])
    print(result_to_json(result) if args.json else render_human_report(result))


if __name__ == "__main__":
    main()
