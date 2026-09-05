"""Pure extraction and chart preparation for selected C4 result evidence."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from mehwar.contracts import EvaluationResult
from mehwar.dashboard.data import is_current_selected_demo

X_AXIS_TITLE = "Column (col)"
Y_AXIS_TITLE = "Row (row)"


@dataclass(frozen=True)
class GridPoint:
    """One scientific (row, col) position prepared for chart coordinates."""

    row: int
    col: int

    @property
    def x(self) -> int:
        """Map chart x to the scientific column coordinate."""
        return self.col

    @property
    def y(self) -> int:
        """Map chart y to the scientific row coordinate."""
        return self.row


@dataclass(frozen=True)
class PathPoint(GridPoint):
    """One ordered position in a supplied controller or reference path."""

    step: int


@dataclass(frozen=True)
class C4VisualizationData:
    """Validated display data extracted without assigning a failure class."""

    grid_size: int
    obstacles: tuple[GridPoint, ...]
    start: GridPoint
    goal: GridPoint
    controller_path: tuple[PathPoint, ...]
    reference_path: tuple[PathPoint, ...]
    repeated_display_points: tuple[GridPoint, ...]
    mission_completed: bool
    supplied_failure_type: str | None
    x_axis_title: str = X_AXIS_TITLE
    y_axis_title: str = Y_AXIS_TITLE


def build_c4_visualization(
    result: EvaluationResult,
) -> C4VisualizationData | None:
    """Extract a selected C4 plot, or return None for non-grid/invalid payloads."""

    if not is_current_selected_demo(result.provenance):
        return None
    if result.scenario_id not in {"C4-0000", "C4-0001"}:
        return None

    grid_size = result.configuration.get("grid_size")
    if isinstance(grid_size, bool) or not isinstance(grid_size, int) or grid_size <= 0:
        return None

    start = _grid_point(result.configuration.get("start"), grid_size)
    goal = _grid_point(result.configuration.get("goal"), grid_size)
    obstacles = _grid_points(result.configuration.get("blocked"), grid_size)
    controller_path = _path_points(result.trajectory, grid_size)
    if start is None or goal is None or obstacles is None or controller_path is None:
        return None

    reference_path: tuple[PathPoint, ...] = ()
    if result.reference_result is not None:
        extracted_reference = _path_points(
            result.reference_result.get("trajectory"), grid_size
        )
        if extracted_reference is not None:
            reference_path = extracted_reference

    repeated_display_points: tuple[GridPoint, ...] = ()
    if result.failure_type == "two_cell_loop":
        counts = Counter((point.row, point.col) for point in controller_path)
        repeated_display_points = tuple(
            GridPoint(row=row, col=col) for row, col in counts if counts[(row, col)] > 1
        )

    return C4VisualizationData(
        grid_size=grid_size,
        obstacles=obstacles,
        start=start,
        goal=goal,
        controller_path=controller_path,
        reference_path=reference_path,
        repeated_display_points=repeated_display_points,
        mission_completed=result.success,
        supplied_failure_type=result.failure_type,
    )


def c4_chart_spec(data: C4VisualizationData) -> dict[str, object]:
    """Return a layered Vega-Lite spec with explicit row/column semantics."""

    domain = [-0.5, data.grid_size - 0.5]
    layers: list[dict[str, object]] = [
        {
            "data": {
                "values": [
                    {
                        "x": domain[0],
                        "x2": domain[1],
                        "y": domain[0],
                        "y2": domain[1],
                    }
                ]
            },
            "mark": {"type": "rect", "fillOpacity": 0, "stroke": "#9ca3af"},
            "encoding": {
                "x2": {"field": "x2"},
                "y2": {"field": "y2"},
            },
        },
        {
            "data": {"values": _point_rows(data.obstacles)},
            "mark": {
                "type": "point",
                "shape": "square",
                "filled": True,
                "size": 90,
                "color": "#374151",
            },
        },
        {
            "data": {"values": _path_rows(data.reference_path)},
            "mark": {
                "type": "line",
                "point": True,
                "strokeDash": [6, 4],
                "color": "#6b7280",
                "strokeWidth": 2,
            },
            "encoding": {"order": {"field": "step", "type": "ordinal"}},
        },
        {
            "data": {"values": _path_rows(data.controller_path)},
            "mark": {
                "type": "line",
                "point": True,
                "color": "#2563eb",
                "strokeWidth": 3,
            },
            "encoding": {"order": {"field": "step", "type": "ordinal"}},
        },
        {
            "data": {"values": _point_rows(data.repeated_display_points)},
            "mark": {
                "type": "point",
                "filled": False,
                "size": 260,
                "stroke": "#dc2626",
                "strokeWidth": 3,
            },
        },
        {
            "data": {"values": _point_rows((data.start,))},
            "mark": {
                "type": "point",
                "shape": "diamond",
                "filled": True,
                "size": 220,
                "color": "#16a34a",
            },
        },
        {
            "data": {"values": _point_rows((data.goal,))},
            "mark": {
                "type": "point",
                "shape": "cross",
                "filled": True,
                "size": 260,
                "color": "#ea580c",
            },
        },
    ]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": "container",
        "height": 520,
        "encoding": {
            "x": {
                "field": "x",
                "type": "quantitative",
                "title": data.x_axis_title,
                "scale": {"domain": domain, "nice": False},
            },
            "y": {
                "field": "y",
                "type": "quantitative",
                "title": data.y_axis_title,
                "scale": {"domain": domain, "nice": False, "reverse": True},
            },
            "tooltip": [
                {"field": "row", "type": "quantitative"},
                {"field": "col", "type": "quantitative"},
                {"field": "step", "type": "ordinal"},
            ],
        },
        "layer": layers,
        "config": {"view": {"stroke": None}},
    }


def _grid_point(value: object, grid_size: int) -> GridPoint | None:
    if (
        not isinstance(value, Sequence)
        or isinstance(value, (str, bytes, bytearray))
        or len(value) != 2
    ):
        return None
    row, col = value
    if any(isinstance(coordinate, bool) for coordinate in (row, col)):
        return None
    if not all(isinstance(coordinate, int) for coordinate in (row, col)):
        return None
    if not (0 <= row < grid_size and 0 <= col < grid_size):
        return None
    return GridPoint(row=row, col=col)


def _grid_points(values: object, grid_size: int) -> tuple[GridPoint, ...] | None:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes, bytearray)):
        return None
    points = tuple(_grid_point(value, grid_size) for value in values)
    if any(point is None for point in points):
        return None
    return tuple(point for point in points if point is not None)


def _path_points(values: object, grid_size: int) -> tuple[PathPoint, ...] | None:
    points = _grid_points(values, grid_size)
    if points is None:
        return None
    return tuple(
        PathPoint(step=step, row=point.row, col=point.col)
        for step, point in enumerate(points)
    )


def _point_rows(points: Sequence[GridPoint]) -> list[dict[str, int]]:
    return [
        {"row": point.row, "col": point.col, "x": point.x, "y": point.y}
        for point in points
    ]


def _path_rows(points: Sequence[PathPoint]) -> list[dict[str, int]]:
    return [
        {
            "step": point.step,
            "row": point.row,
            "col": point.col,
            "x": point.x,
            "y": point.y,
        }
        for point in points
    ]
