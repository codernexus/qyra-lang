# Contributing to Qyra

Qyra is in early alpha. Changes to syntax or semantics must include:

1. a clear motivation;
2. tests for valid and invalid programs;
3. documentation updates;
4. no false claims of production readiness.

## Local setup

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1
pip install -e .
python -m unittest discover -s tests -v
```

Founder and Lead Language Designer: **Трифон Ярослав Владимирович (Nexu_scoder)**.
