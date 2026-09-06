"""One-page Streamlit presentation of one supplied EvaluationResult."""

from __future__ import annotations

import streamlit as st

from mehwar.contracts import EvaluationResult, JsonValue
from mehwar.dashboard.data import (
    CURRENT_DEMO_LABEL,
    REFERENCE_UNAVAILABLE_MESSAGE,
    SUPPLIED_CURRENT_DEMO_LABEL,
    SYNTHETIC_FIXTURE_LABEL,
    DashboardDataError,
    build_run_summary,
    default_fixture_path,
    extract_coordinate_trajectory,
    is_current_selected_demo,
    is_synthetic_or_non_research,
    load_evaluation_result,
    ordered_trajectory_rows,
)
from mehwar.dashboard.local_demo import (
    checkpoint_path_from_environment,
    run_local_c4_demo,
    run_selected_c4_batch,
)
from mehwar.dashboard.visualization import build_c4_visualization, c4_chart_spec
from mehwar.evidence import EvidenceProfile, build_evidence_profile
from mehwar.reporting import DEFAULT_LIMITATIONS

FIXTURE_INPUT = "Bundled synthetic engineering fixture"
UPLOAD_INPUT = "Uploaded EvaluationResult JSON"
LOCAL_INPUT = "Run selected verified C4 demo locally"


def main() -> None:
    """Render fixture, uploaded, and locally executed results through one path."""

    st.set_page_config(
        page_title="MEHWAR | Evaluation Evidence",
        page_icon="M",
        layout="wide",
    )
    # Keep the evidence and trajectory readable at ordinary desktop zoom.
    st.html("""
        <style>
        .stMainBlockContainer { padding-top: 2rem; }
        [data-testid="stMetricValue"] { font-size: 1.5rem; }
        </style>
    """)
    st.title("MEHWAR")
    st.caption(
        "Navigation-controller capability-boundary and mission-liveness evaluation"
    )

    st.markdown(
        "**Legal action selection does not by itself guarantee mission liveness.**"
    )

    result, source_label, batch_results, locally_executed = _load_selected_result()
    synthetic = is_synthetic_or_non_research(result.provenance)
    _render_evidence_banner(
        synthetic=synthetic,
        source_label=source_label,
        selected_demo=is_current_selected_demo(result.provenance),
        locally_executed=locally_executed,
    )
    if is_current_selected_demo(result.provenance):
        _render_selected_demo_counts(result)
    _render_run_summary(result)
    _render_trajectory(result)
    with st.expander("Controller metadata", expanded=False):
        st.write(f"Controller: {result.controller}")
        st.write(f"Scenario family: {result.scenario_family}")
        st.write(f"Trajectory records: {len(result.trajectory)}")
        _render_mapping(
            result.controller_metadata, empty_message="No metadata supplied."
        )
    with st.expander("Diagnostics", expanded=False):
        _render_json_section("Diagnostics", result.diagnostics)
    with st.expander("Deterministic reference — full supplied record", expanded=False):
        _render_reference(result)
    with st.expander("Configuration", expanded=False):
        _render_json_section("Configuration", result.configuration)
    with st.expander("Provenance", expanded=False):
        _render_provenance(result.provenance)
    with st.expander("Evidence limitations — read before interpreting", expanded=False):
        _render_limitations(synthetic=synthetic)
    if batch_results is not None:
        with st.expander("Selected demo set evidence profile", expanded=False):
            _render_selected_demo_profile(batch_results)


def _load_selected_result() -> tuple[
    EvaluationResult, str, tuple[EvaluationResult, ...] | None, bool
]:
    st.sidebar.header("Evaluation input")
    input_mode = st.sidebar.radio(
        "Input source",
        [FIXTURE_INPUT, UPLOAD_INPUT, LOCAL_INPUT],
    )
    try:
        if input_mode == FIXTURE_INPUT:
            fixture_path = default_fixture_path()
            return load_evaluation_result(fixture_path), fixture_path.name, None, False
        if input_mode == LOCAL_INPUT:
            return _load_local_demo()
        upload = st.sidebar.file_uploader("EvaluationResult JSON", type=["json"])
        if upload is None:
            st.info("Upload an EvaluationResult JSON file to display its evidence.")
            st.stop()
        return load_evaluation_result(upload.getvalue()), upload.name, None, False
    except DashboardDataError as exc:
        st.error(str(exc))
        st.stop()


def _load_local_demo() -> tuple[
    EvaluationResult, str, tuple[EvaluationResult, ...] | None, bool
]:
    scenario_id = st.sidebar.selectbox("Selected C4 scenario", ["C4-0000", "C4-0001"])
    checkpoint = checkpoint_path_from_environment()
    if st.sidebar.button("Run verified C4 demo"):
        # Never retain an old result if a new execution fails.
        st.session_state.pop("local_c4_result", None)
        with st.spinner("Running the selected C4 demo locally..."):
            result = run_local_c4_demo(scenario_id)
        st.session_state["local_c4_result"] = (scenario_id, checkpoint, result)
    if st.sidebar.button("Run selected demo set"):
        st.session_state.pop("local_c4_result", None)
        st.session_state.pop("selected_c4_batch", None)
        with st.spinner("Running C4-0000 and C4-0001 locally..."):
            batch_results = run_selected_c4_batch()
        st.session_state["selected_c4_batch"] = (checkpoint, batch_results)

    stored_batch = st.session_state.get("selected_c4_batch")
    batch_results = (
        stored_batch[1]
        if stored_batch is not None and stored_batch[0] == checkpoint
        else None
    )
    stored = st.session_state.get("local_c4_result")
    if stored is not None and stored[:2] == (scenario_id, checkpoint):
        result = stored[2]
    elif batch_results is not None:
        result = next(
            result for result in batch_results if result.scenario_id == scenario_id
        )
    else:
        st.info(
            "Select a scenario and click Run verified C4 demo, or run the selected "
            "demo set."
        )
        st.stop()
    return result, f"Local verified seed-33 / {scenario_id}", batch_results, True


def _render_evidence_banner(
    *,
    synthetic: bool,
    source_label: str,
    selected_demo: bool = False,
    locally_executed: bool = False,
) -> None:
    if synthetic:
        st.warning(
            f"**{SYNTHETIC_FIXTURE_LABEL}**\n\n"
            "This payload is labeled synthetic/non-research evidence. It must not "
            "be interpreted as PPO, C4, research-replication, safety, or "
            "product-performance evidence."
        )
    elif selected_demo:
        if locally_executed:
            st.info(
                f"**{CURRENT_DEMO_LABEL}**\n\n"
                "Selected development-validation scenario; not a fresh holdout. "
                "This single run does not establish general controller performance."
            )
        else:
            st.info(
                f"**{SUPPLIED_CURRENT_DEMO_LABEL}**\n\n"
                "The current-demo classification is taken from the uploaded payload "
                "and its provenance. MEHWAR did not independently execute or verify "
                "this run during this dashboard session."
            )
    else:
        st.info(
            "Evidence classification is taken from the supplied payload. Inspect "
            "provenance and limitations before drawing conclusions."
        )
    st.sidebar.caption(f"Selected input: `{source_label}`")


def _render_selected_demo_counts(result: EvaluationResult) -> None:
    """Show single-run evidence beside a descriptive status, without a score."""
    profile = build_evidence_profile((result,))
    if result.success:
        evidence_label = "NO FAILURE OBSERVED IN SELECTED DEMO RUN"
    elif result.failure_type in ("two_cell_loop", "longer_loop", "timeout_other"):
        evidence_label = "LIVENESS DEGRADATION OBSERVED"
    else:
        evidence_label = "FAILURE OBSERVED IN SELECTED DEMO RUN"
    st.markdown(f"**{evidence_label}**")
    successes = profile.mission_completions
    loop_count = profile.failure_type_counts.get("two_cell_loop", 0)
    collisions = profile.failure_type_counts.get("collision", 0)
    invalid = (
        profile.invalid_actions_total if profile.invalid_actions_complete else "unknown"
    )
    st.write(
        f"1 selected run | {successes} {'success' if successes else 'successes'} | "
        f"{profile.mission_failures} observed failures | {loop_count} two_cell_loop | "
        f"{collisions} collisions | {invalid} invalid actions"
    )


def _render_selected_demo_profile(
    results: tuple[EvaluationResult, ...],
) -> None:
    profile = build_evidence_profile(results)
    st.subheader("Selected demo set evidence profile")
    st.markdown(f"### {profile.evidence_label}")
    st.caption(
        "Selected current MVP demo set; development-validation classification; "
        "fresh_holdout is false. Raw counts describe only these selected "
        "demonstrations, not a fresh holdout or general performance estimate."
    )

    counts = st.columns(4)
    counts[0].metric("Scenarios evaluated", str(profile.scenarios_evaluated))
    counts[1].metric("Mission completions", str(profile.mission_completions))
    counts[2].metric("Mission failures", str(profile.mission_failures))
    counts[3].metric("Reference completions", str(profile.reference_completions))
    st.write(f"Scenario IDs: {', '.join(profile.scenario_ids)}")
    st.write(
        "Supplied failure-type counts: "
        f"two_cell_loop={profile.failure_type_counts.get('two_cell_loop', 0)} | "
        f"longer_loop={profile.failure_type_counts.get('longer_loop', 0)} | "
        f"timeout_other={profile.failure_type_counts.get('timeout_other', 0)} | "
        f"collision={profile.failure_type_counts.get('collision', 0)}"
    )
    st.caption(f"All supplied failure types: {_format_failure_counts(profile)}")
    invalid_actions = (
        str(profile.invalid_actions_total)
        if profile.invalid_actions_complete
        else "unknown (incomplete diagnostics)"
    )
    st.write(f"Invalid actions: {invalid_actions}")
    st.write(
        "Deterministic references available: "
        f"{profile.reference_results_available}; completed: "
        f"{profile.reference_completions}"
    )
    st.caption(
        "Each EvaluationResult below retains its own controller metadata, "
        "configuration, trajectory, reference result, diagnostics, and provenance."
    )
    for result in results:
        with st.expander(f"Individual EvaluationResult — {result.scenario_id}"):
            st.json(result.to_dict())


def _format_failure_counts(profile: EvidenceProfile) -> str:
    return (
        ", ".join(
            f"{failure_type if failure_type is not None else 'null'}={count}"
            for failure_type, count in profile.failure_type_counts.items()
        )
        or "none supplied"
    )


def _render_run_summary(result: EvaluationResult) -> None:
    summary = build_run_summary(result)
    first_row = st.columns(4)
    first_row[0].metric("Scenario", summary.scenario_id)
    first_row[1].metric("Mission outcome", summary.mission_outcome)
    first_row[2].metric("Steps", str(summary.steps))
    first_row[3].metric(
        "Failure type",
        summary.failure_type if summary.failure_type is not None else "Not supplied",
    )

    context = st.columns(4)
    context[0].markdown("Invalid actions")
    context[0].write(str(result.diagnostics.get("invalid_actions", "Not supplied")))
    context[1].markdown("Controller path cost")
    context[1].write(str(summary.path_cost))
    reference = result.reference_result
    if reference is not None and reference.get("planner") == "A*":
        context[2].markdown("A* reference steps")
        context[2].write(str(reference.get("steps", "Not supplied")))
        context[3].markdown("A* reference cost")
        context[3].write(str(reference.get("cost", "Not supplied")))
        st.caption(
            "deterministic A* reliability reference under the shared grid contract"
        )
    elif reference is None:
        st.info(REFERENCE_UNAVAILABLE_MESSAGE)
    else:
        st.caption("Reference data is available in the full supplied record below.")


def _render_trajectory(result: EvaluationResult) -> None:
    st.subheader("Trajectory evidence")
    c4_visualization = build_c4_visualization(result)
    if c4_visualization is not None:
        _render_c4_trajectory(c4_visualization)
        return

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


def _render_c4_trajectory(visualization) -> None:
    st.caption(
        "Scientific positions are (row, col); the chart maps x = col and y = row. "
        "Blue: learned-controller path. Gray dashed: supplied deterministic A* "
        "reference. Dark squares: obstacles. Green diamond: start. Orange cross: "
        "goal. Red rings: repeated cells shown only for a supplied two_cell_loop "
        "result."
    )
    spec = c4_chart_spec(visualization)
    spec["height"] = 380  # Presentation sizing only; all scientific layers stay intact.
    st.vega_lite_chart(spec, width="stretch")


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
        *DEFAULT_LIMITATIONS,
    ]
    if synthetic:
        limitations.append(
            "Fixture data does not constitute research or product-performance evidence."
        )
    st.warning("\n".join(f"- {limitation}" for limitation in limitations))
