# Installation

Qyra 0.3.0-alpha currently requires Python 3.10 or newer.

## Install from source

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .
qyra check examples/typed.qy
qyra run examples/typed.qy
```

## Run without installation

```bash
python -m qyra.cli check examples/typed.qy
python -m qyra.cli run examples/typed.qy
```
