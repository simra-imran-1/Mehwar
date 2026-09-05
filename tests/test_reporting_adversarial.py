import json

import pytest

from mehwar import EvaluationResult
from mehwar.dashboard.data import default_fixture_path, load_evaluation_result
from mehwar.reporting import DEFAULT_LIMITATIONS, render_human_report, result_to_json


@pytest.fixture
def payload():
    return json.loads(default_fixture_path().read_text(encoding="utf-8"))


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
@pytest.mark.parametrize("field", ["path_cost", "diagnostics", "provenance"])
def test_json_export_rejects_nonfinite_values_in_scalar_and_nested_fields(
    payload, field, value,
):
    payload[field] = value if field == "path_cost" else {"nested": [{"value": value}]}
    with pytest.raises(ValueError, match="Out of range float values"):
        result_to_json(EvaluationResult(**payload))


def test_json_round_trip_preserves_nested_unicode_provenance_and_unknown_values(
    payload,
):
    payload.update(
        controller_metadata={"checkpoint": None, "parameters": [1, True, {"x": 1.5}]},
        trajectory=[None, {"event": "آغاز", "cell": [2, 3]}, "finish"],
        provenance={
            "source": "محوَر", "unknown_commit": None, "extra": {"list": [1, 2]},
        },
    )
    result = EvaluationResult(**payload)
    serialized = result_to_json(result)

    assert load_evaluation_result(serialized.encode()) == result
    assert json.loads(serialized) == payload
    assert "محوَر" in serialized
    # Mutating an exported copy must not alter the evidence held by the result.
    exported = result.to_dict()
    exported["provenance"]["extra"]["list"].append(3)
    assert result.provenance["extra"] == {"list": [1, 2]}


@pytest.mark.parametrize("success", [True, False])
def test_human_report_keeps_limitations_for_unclassified_runs(payload, success):
    payload.update(success=success, provenance={})
    report = render_human_report(EvaluationResult(**payload))
    for limitation in DEFAULT_LIMITATIONS:
        assert limitation in report
    assert "Provenance: {}" in report
