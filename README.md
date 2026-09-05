# MEHWAR

MEHWAR is a controller-agnostic evaluation layer for characterizing navigation-controller capability boundaries and mission-liveness failures. Its shared contracts and evaluator feed an engineer-facing dashboard without coupling presentation code to controller or failure-classification logic.

## Setup and verification

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest
```

## Fixture-driven dashboard

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

The dashboard loads `fixtures/sample_evaluation_result.json` by default and can display an uploaded EvaluationResult-compatible JSON file. The bundled sample is **synthetic engineering fixture data for UI/integration testing only**. It is not PPO output, C4 research output, research replication, or product-performance evidence. The dashboard displays runner-supplied results and does not classify failures or execute a controller, A*, or a simulator.

MEHWAR has no flight validation, no safety certification, and no deployment approval.
