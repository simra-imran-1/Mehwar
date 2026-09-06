"""One-page Streamlit presentation of one supplied EvaluationResult."""

from __future__ import annotations

from html import escape

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
from mehwar.dashboard.theme import WORKSPACE_CSS
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
    st.html(WORKSPACE_CSS)
    with st.container(key="identity"):
        brand, purpose, stage = st.columns([1, 3.4, 1.4], vertical_alignment="center")
        with brand:
            st.title("MEHWAR")
        with purpose:
            st.markdown(
                '<div class="mw-descriptor">Navigation-controller capability-boundary '
                "and mission-liveness evaluation</div>",
                unsafe_allow_html=True,
            )
        with stage:
            st.markdown(
                '<div class="mw-prototype">Research-backed<br>'
                "Functional prototype</div>",
                unsafe_allow_html=True,
            )
    with st.container(key="thesis"):
        st.markdown(
            "**Legal action selection does not by itself guarantee mission liveness.**"
        )

    result, source_label, batch_results, locally_executed = _load_selected_result()
    synthetic = is_synthetic_or_non_research(result.provenance)
    with st.container(key="evidence-banner"):
        _render_evidence_banner(
            synthetic=synthetic,
            source_label=source_label,
            selected_demo=is_current_selected_demo(result.provenance),
            locally_executed=locally_executed,
        )
    with st.container(key="evidence-workspace"):
        trajectory, reading = st.columns([1.85, 1], gap="large")
        with trajectory:
            with st.container(key="trajectory-panel"):
                _render_trajectory(result)
        with reading:
            with st.container(key="run-summary"):
                raw_counts = _render_run_summary(result)
            with st.container(key="reference-context"):
                _render_reference_context(result)
    if raw_counts is not None:
        with st.container(key="raw-context"):
            st.write(raw_counts)
    st.markdown(
        '<div class="mw-record-heading"><h2>Evidence record</h2>'
        "<p>Inspect the supplied records, provenance and interpretation limits.</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    detail_left, detail_right = st.columns(2)
    with detail_left:
        with st.expander("Controller metadata", expanded=False):
            st.write(f"Controller: {result.controller}")
            st.write(f"Scenario family: {result.scenario_family}")
            st.write(f"Trajectory records: {len(result.trajectory)}")
            st.write(f"Controller path cost (supplied): {result.path_cost}")
            _render_mapping(
                result.controller_metadata, empty_message="No metadata supplied."
            )
        with st.expander("Diagnostics", expanded=False):
            _render_json_section("Diagnostics", result.diagnostics)
        with st.expander(
            "Deterministic reference — full supplied record", expanded=False
        ):
            _render_reference(result)
    with detail_right:
        with st.expander("Configuration", expanded=False):
            _render_json_section("Configuration", result.configuration)
        with st.expander("Provenance", expanded=False):
            _render_provenance(result.provenance)
        with st.expander(
            "Evidence limitations — read before interpreting",
            expanded=False,
        ):
            _render_limitations(synthetic=synthetic)
    if batch_results is not None:
        with st.expander("Selected demo set evidence profile", expanded=False):
            _render_selected_demo_profile(batch_results)


def _load_selected_result() -> tuple[
    EvaluationResult, str, tuple[EvaluationResult, ...] | None, bool
]:
    st.sidebar.markdown(
        '<div class="mw-rail-brand">MEHWAR<strong>Evaluation workspace</strong></div>',
        unsafe_allow_html=True,
    )
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
    if st.sidebar.button("Run verified C4 demo", type="primary"):
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


def _render_selected_demo_counts(result: EvaluationResult) -> str:
    """Show single-run evidence beside a descriptive status, without a score."""
    profile = build_evidence_profile((result,))
    if result.success:
        evidence_label = "NO FAILURE OBSERVED IN SELECTED DEMO RUN"
    elif result.failure_type in ("two_cell_loop", "longer_loop", "timeout_other"):
        evidence_label = "LIVENESS DEGRADATION OBSERVED"
    else:
        evidence_label = "FAILURE OBSERVED IN SELECTED DEMO RUN"
    status_key = "evidence-status" if result.success else "evidence-status-observed"
    with st.container(key=status_key):
        st.markdown(f"**{evidence_label}**")
    successes = profile.mission_completions
    loop_count = profile.failure_type_counts.get("two_cell_loop", 0)
    collisions = profile.failure_type_counts.get("collision", 0)
    invalid = (
        profile.invalid_actions_total if profile.invalid_actions_complete else "unknown"
    )
    return (
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


def _render_run_summary(result: EvaluationResult) -> str | None:
    """Present supplied values; styling never assigns a scientific classification."""
    summary = build_run_summary(result)
    st.markdown(
        '<div class="mw-eyebrow">Controller evidence · Mission outcome</div>'
        f'<h2 class="mw-outcome">{escape(summary.mission_outcome)}</h2>',
        unsafe_allow_html=True,
    )
    raw_counts = (
        _render_selected_demo_counts(result)
        if is_current_selected_demo(result.provenance)
        else None
    )
    invalid = result.diagnostics.get("invalid_actions", "Not supplied")
    if not result.success and invalid == 0 and result.failure_type == "two_cell_loop":
        st.caption("0 invalid actions · mission still failed through legal recurrence")
    failure = (
        summary.failure_type if summary.failure_type is not None else "Not supplied"
    )
    st.markdown(
        '<dl class="mw-measures">'
        f"<div><dt>Steps</dt><dd>{summary.steps}</dd></div>"
        f"<div><dt>Invalid actions</dt><dd>{escape(str(invalid))}</dd></div></dl>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<dl class="mw-record">'
        f"<div><dt>Failure type</dt><dd>{escape(failure)}</dd></div>"
        "<div><dt>Controller path cost</dt>"
        f"<dd>{escape(_display_cost(summary.path_cost))}</dd></div>"
        "<div><dt>Controller</dt>"
        f'<dd class="mw-identity">{escape(summary.controller)}</dd></div></dl>',
        unsafe_allow_html=True,
    )
    return raw_counts


def _display_cost(value: object) -> str:
    """Round numeric costs only in the hero; retain supplied records verbatim."""
    return f"{value:.3f}" if type(value) in (int, float) else str(value)


def _render_reference_context(result: EvaluationResult) -> None:
    reference = result.reference_result
    st.markdown(
        '<div class="mw-eyebrow">Reference context</div>'
        '<h3 class="mw-reference-title">Deterministic reference</h3>',
        unsafe_allow_html=True,
    )
    if reference is not None and reference.get("planner") == "A*":
        st.caption(
            "deterministic A* reliability reference under the shared grid contract"
        )
        st.markdown(
            '<dl class="mw-reference"><div><dt>A* reference steps</dt>'
            f"<dd>{escape(str(reference.get('steps', 'Not supplied')))}</dd></div>"
            "<div><dt>A* reference cost</dt>"
            f"<dd>{escape(_display_cost(reference.get('cost', 'Not supplied')))}</dd>"
            "</div></dl>",
            unsafe_allow_html=True,
        )
    elif reference is None:
        st.info(REFERENCE_UNAVAILABLE_MESSAGE)
    else:
        st.caption("Reference data is available in the full supplied record below.")


def _render_trajectory(result: EvaluationResult) -> None:
    c4_visualization = build_c4_visualization(result)
    family_label = (
        "STRUCTURED C4 SCENARIO"
        if c4_visualization is not None
        else result.scenario_family
    )
    st.markdown(
        '<div class="mw-panel-heading"><div>'
        '<div class="mw-eyebrow">Trajectory evidence</div>'
        f"<h2>Scenario {escape(result.scenario_id)}</h2></div>"
        f'<span class="mw-tag">{escape(family_label)}</span></div>',
        unsafe_allow_html=True,
    )
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
    spec = c4_chart_spec(visualization)
    # Presentation only: preserve every point, encoding and tooltip.
    if visualization.repeated_display_points:
        spec["layer"][4]["mark"].update(size=360, strokeWidth=3.5)
    spec["height"] = 420
    spec["background"] = "#ffffff"
    spec["config"] = {
        "view": {"stroke": None},
        "axis": {
            "labelColor": "#546974",
            "titleColor": "#304e60",
            "gridColor": "#e5ebed",
            "domainColor": "#cad5da",
            "tickColor": "#cad5da",
            "labelFont": "Arial",
            "titleFont": "Arial",
            "labelFontSize": 11,
            "titleFontSize": 12,
            "titlePadding": 12,
        },
    }
    st.vega_lite_chart(spec, width="stretch", theme=None)
    st.markdown(
        '<div class="mw-legend" aria-label="Trajectory legend">'
        '<span><i aria-hidden="true"></i>Learned-controller path</span>'
        '<span><i class="reference" aria-hidden="true"></i>Supplied A* reference</span>'
        '<span><i class="obstacle" aria-hidden="true"></i>Obstacles</span>'
        '<span><i class="start" aria-hidden="true"></i>Start</span>'
        '<span><i class="goal" aria-hidden="true">+</i>Goal</span>'
        '<span><i class="recurrence" aria-hidden="true"></i>Repeated cells</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Scientific positions are (row, col); the chart maps x = col and y = row. "
        "Red rings show repeated cells only for a supplied two_cell_loop result."
    )


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
