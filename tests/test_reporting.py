import json
from pathlib import Path

from mehwar.contracts import EvaluationResult
from mehwar.reporting import DEFAULT_LIMITATIONS, render_human_report, result_to_json


def sample_result():
    path = (
        Path(__file__).resolve().parents[1] / "fixtures/sample_evaluation_result.json"
    )
    return EvaluationResult(**json.loads(path.read_text(encoding="utf-8")))


def test_json_round_trip_preserves_contract_and_provenance():
    result = sample_result()
    before = result.to_dict()
    assert json.loads(result_to_json(result)) == before
    assert result.to_dict() == before


def test_human_report_displays_all_evidence_and_limitations():
    result = sample_result()
    report = render_human_report(result)
    for label in ("Controller:", "Scenario:", "Outcome:", "Failure type:", "Steps:",
                  "Path cost:", "A* reference:", "Diagnostics:", "Provenance:",
                  "Limitations:"):
        assert label in report
    assert result.controller in report and result.scenario_id in report
    assert "synthetic-engineering-sample" in report
    for limitation in DEFAULT_LIMITATIONS:
        assert limitation in report


def test_absent_provenance_is_not_invented():
    payload = sample_result().to_dict()
    payload.update(provenance={}, controller_metadata={}, reference_result=None)
    report = render_human_report(EvaluationResult(**payload))
    assert "Provenance: {}" in report
    assert "A* reference: Not supplied" in report
    assert "seed" not in report and "checkpoint_sha256" not in report
