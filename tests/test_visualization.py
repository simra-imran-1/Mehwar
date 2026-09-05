from dataclasses import replace

from mehwar.contracts import EvaluationResult
from mehwar.dashboard.data import default_fixture_path, load_evaluation_result
from mehwar.dashboard.visualization import (
    X_AXIS_TITLE,
    Y_AXIS_TITLE,
    build_c4_visualization,
    c4_chart_spec,
)


def selected_c4_result() -> EvaluationResult:
    return EvaluationResult(
        controller="visualization-test-controller",
        controller_metadata={},
        scenario_id="C4-0001",
        scenario_family="u_trap",
        success=False,
        steps=4,
        path_cost=4.0,
        failure_type="two_cell_loop",
        trajectory=[[8, 9], [9, 9], [8, 9], [9, 9]],
        reference_result={
            "planner": "A*",
            "found": True,
            "trajectory": [[8, 9], [9, 8], [10, 7], [13, 1]],
        },
        diagnostics={"invalid_actions": 0},
        configuration={
            "grid_size": 15,
            "blocked": [[4, 8], [4, 9], [10, 11]],
            "start": [8, 9],
            "goal": [13, 1],
        },
        provenance={
            "data_classification": "current-mehwar-selected-demo-run",
            "scenario_selection": "selected current MVP demo",
            "scenario_classification": "development_validation",
            "fresh_holdout": False,
        },
    )


def test_scientific_row_col_maps_to_x_col_and_y_row():
    visualization = build_c4_visualization(selected_c4_result())

    assert visualization is not None
    first = visualization.controller_path[0]
    assert (first.row, first.col) == (8, 9)
    assert (first.x, first.y) == (9, 8)
    assert visualization.x_axis_title == X_AXIS_TITLE == "Column (col)"
    assert visualization.y_axis_title == Y_AXIS_TITLE == "Row (row)"


def test_selected_c4_grid_obstacles_start_goal_and_paths_are_extracted():
    visualization = build_c4_visualization(selected_c4_result())

    assert visualization is not None
    assert visualization.grid_size == 15
    assert [(point.row, point.col) for point in visualization.obstacles] == [
        (4, 8),
        (4, 9),
        (10, 11),
    ]
    assert (visualization.start.row, visualization.start.col) == (8, 9)
    assert (visualization.goal.row, visualization.goal.col) == (13, 1)
    assert [(point.row, point.col) for point in visualization.controller_path] == [
        (8, 9),
        (9, 9),
        (8, 9),
        (9, 9),
    ]
    assert [(point.row, point.col) for point in visualization.reference_path] == [
        (8, 9),
        (9, 8),
        (10, 7),
        (13, 1),
    ]


def test_supplied_two_cell_result_exposes_repeated_display_region():
    visualization = build_c4_visualization(selected_c4_result())

    assert visualization is not None
    assert [
        (point.row, point.col) for point in visualization.repeated_display_points
    ] == [
        (8, 9),
        (9, 9),
    ]


def test_visualization_never_recomputes_failure_type_from_repeated_path():
    result = replace(selected_c4_result(), failure_type="timeout_other")

    visualization = build_c4_visualization(result)

    assert visualization is not None
    assert visualization.supplied_failure_type == "timeout_other"
    assert visualization.repeated_display_points == ()


def test_chart_spec_has_explicit_grid_extent_axes_and_all_real_layers():
    visualization = build_c4_visualization(selected_c4_result())
    assert visualization is not None

    spec = c4_chart_spec(visualization)

    assert spec["encoding"]["x"]["title"] == "Column (col)"
    assert spec["encoding"]["y"]["title"] == "Row (row)"
    assert spec["encoding"]["x"]["scale"]["domain"] == [-0.5, 14.5]
    assert spec["encoding"]["y"]["scale"]["reverse"] is True
    layers = spec["layer"]
    assert len(layers[1]["data"]["values"]) == 3  # obstacles
    assert len(layers[2]["data"]["values"]) == 4  # supplied A* path
    assert len(layers[3]["data"]["values"]) == 4  # controller path
    assert len(layers[4]["data"]["values"]) == 2  # repeated display cells
    assert layers[5]["data"]["values"][0]["x"] == 9  # start col
    assert layers[6]["data"]["values"][0]["y"] == 13  # goal row


def test_missing_reference_is_not_fabricated():
    result = replace(selected_c4_result(), reference_result=None)

    visualization = build_c4_visualization(result)

    assert visualization is not None
    assert visualization.reference_path == ()


def test_generic_fixture_and_malformed_grid_payload_remain_safe():
    fixture = load_evaluation_result(default_fixture_path())
    assert build_c4_visualization(fixture) is None

    malformed = replace(selected_c4_result(), trajectory=["not-a-grid-position"])
    assert build_c4_visualization(malformed) is None
