# MEHWAR

MEHWAR is a controller-agnostic evaluation layer for characterizing navigation-controller capability boundaries and mission-liveness failures. The current T1 baseline freezes the generic controller and evaluation-result contracts needed by later assurance and dashboard work.

## Setup and verification

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest
```

This baseline contains contracts and one clearly labeled synthetic engineering fixture only. It does not contain a scenario runner, evaluator, failure detector, PPO adapter, A* implementation, dashboard, or end-to-end demo.

MEHWAR has no flight validation, no safety certification, and no deployment approval.
