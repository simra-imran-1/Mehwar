"""Pure data preparation and Streamlit rendering for MEHWAR results."""

from mehwar.dashboard.data import (
    REFERENCE_UNAVAILABLE_MESSAGE,
    SYNTHETIC_FIXTURE_LABEL,
    DashboardDataError,
    RunSummary,
    build_run_summary,
    extract_coordinate_trajectory,
    is_synthetic_or_non_research,
    load_evaluation_result,
)

__all__ = [
    "REFERENCE_UNAVAILABLE_MESSAGE",
    "SYNTHETIC_FIXTURE_LABEL",
    "DashboardDataError",
    "RunSummary",
    "build_run_summary",
    "extract_coordinate_trajectory",
    "is_synthetic_or_non_research",
    "load_evaluation_result",
]
