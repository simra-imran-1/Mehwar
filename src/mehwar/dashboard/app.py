"""One-page Streamlit presentation of one supplied EvaluationResult."""

from __future__ import annotations

import streamlit as st

from mehwar.contracts import EvaluationResult, JsonValue
from mehwar.dashboard.data import (
    REFERENCE_UNAVAILABLE_MESSAGE,
    SYNTHETIC_FIXTURE_LABEL,
    DashboardDataError,
    build_run_summary,
    default_fixture_path,
    extract_coordinate_trajectory,
    is_synthetic_or_non_research,
    load_evaluation_result,
    ordered_trajectory_rows,
)


def main() -> None:
    """Render the fixture-driven MEHWAR dashboard."""

    st.set_page_config(
        page_title="MEHWAR | Evaluation Evidence",
        page_icon="M",
        layout="wide",
    )
    st.title("MEHWAR")
    st.caption(
        "Navigation-controller capability-boundary and mission-liveness evaluation"
    )

    result, source_label = _load_selected_result()
    synthetic = is_synthetic_or_non_research(result.provenance)
    _render_evidence_banner(synthetic=synthetic, source_label=source_label)
    _render_run_summary(result)
    _render_trajectory(result)
    _render_reference(result)
    _render_json_section("Diagnostics", result.diagnostics)
    _render_json_section("Configuration", result.configuration)
    _render_provenance(result.provenance)
    _render_limitations(synthetic=synthetic)


def _load_selected_result() -> tuple[EvaluationResult, str]:
    st.sidebar.header("Evaluation input")
    upload = st.sidebar.file_uploader(
        "EvaluationResult JSON (optional)",
        type=["json"],
        help="Leave empty to use the repository's synthetic sample fixture.",
    )

    try:
        if upload is None:
            fixture_path = default_fixture_path()
            return load_evaluation_result(fixture_path), fixture_path.name
        return load_evaluation_result(upload.getvalue()), upload.name
    except DashboardDataError as exc:
        st.error(str(exc))
        st.stop()


def _render_evidence_banner(*, synthetic: bool, source_label: str) -> None:
    if synthetic:
        st.warning(
            f"### {SYNTHETIC_FIXTURE_LABEL}\n"
            "This payload is labeled synthetic/non-research evidence. It must not "
            "be interpreted as PPO, C4, research-replication, safety, or "
            "product-performance evidence."
        )
    else:
        st.info(
            "Evidence classification is taken from the supplied payload. Inspect "
            "provenance and limitations before drawing conclusions."
        )
    st.caption(f"Selected input: `{source_label}`")


def _render_run_summary(result: EvaluationResult) -> None:
    summary = build_run_summary(result)
    st.subheader("Run summary")

    first_row = st.columns(4)
    first_row[0].metric("Controller", summary.controller)
    first_row[1].metric("Scenario", summary.scenario_id)
    first_row[2].metric("Scenario family", summary.scenario_family)
    first_row[3].metric("Mission outcome", summary.mission_outcome)

    second_row = st.columns(4)
    second_row[0].metric("Steps", str(summary.steps))
    second_row[1].metric("Path cost", f"{summary.path_cost:g}")
    second_row[2].metric(
        "Failure type",
        summary.failure_type if summary.failure_type is not None else "Not supplied",
    )
    second_row[3].metric("Trajectory records", str(len(result.trajectory)))

    st.markdown("**Controller metadata**")
    _render_mapping(result.controller_metadata, empty_message="No metadata supplied.")


def _render_trajectory(result: EvaluationResult) -> None:
    st.subheader("Trajectory evidence")
    coordinates = extract_coordinate_trajectory(result.trajectory)
    if coordinates is not None:
        plot_rows = [
            {"step": point.step, "x": point.x, "y": point.y} for point in coordinates
        ]
        st.caption(
            "A 2-D path is shown because every recorded state contained one "
            "uniform, finite coordinate pair."
        )
        st.vega_lite_chart(
            plot_rows,
            {
                "mark": {"type": "line", "point": True},
                "encoding": {
                    "x": {"field": "x", "type": "quantitative"},
                    "y": {"field": "y", "type": "quantitative"},
                    "order": {"field": "step", "type": "ordinal"},
                    "tooltip": [
                        {"field": "step", "type": "ordinal"},
                        {"field": "x", "type": "quantitative"},
                        {"field": "y", "type": "quantitative"},
                    ],
                },
            },
            width="stretch",
        )
    else:
        st.caption(
            "The trajectory is not assumed to be grid data; recorded states/events "
            "are shown in order."
        )

    rows = ordered_trajectory_rows(result.trajectory)
    if rows:
        st.dataframe(rows, width="stretch", hide_index=True)
    else:
        st.info("No trajectory records were supplied for this run.")


def _render_reference(result: EvaluationResult) -> None:
    st.subheader("Deterministic reference result")
    if result.reference_result is None:
        st.info(REFERENCE_UNAVAILABLE_MESSAGE)
        return
    st.caption(
        "Reference data below is displayed exactly as supplied by the evaluation "
        "payload."
    )
    st.json(result.reference_result)


def _render_json_section(title: str, values: dict[str, JsonValue]) -> None:
    st.subheader(title)
    _render_mapping(values, empty_message=f"No {title.lower()} supplied for this run.")


def _render_provenance(provenance: dict[str, JsonValue]) -> None:
    st.subheader("Provenance")
    st.caption(
        "Missing identifiers remain unknown; the dashboard does not create hashes, "
        "timestamps, protocol identities, or run IDs."
    )
    _render_mapping(
        provenance,
        empty_message="Provenance not supplied for this run; values are unknown.",
    )


def _render_mapping(values: dict[str, JsonValue], *, empty_message: str) -> None:
    if values:
        st.json(values)
    else:
        st.info(empty_message)


def _render_limitations(*, synthetic: bool) -> None:
    st.subheader("Evidence limitations")
    limitations = [
        "This view represents only the selected fixture or current run.",
        "No flight validation.",
        "No safety certification.",
        "No deployment approval.",
    ]
    if synthetic:
        limitations.append(
            "Fixture data does not constitute research or product-performance evidence."
        )
    st.warning("\n".join(f"- {limitation}" for limitation in limitations))
