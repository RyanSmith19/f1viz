PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/python -m pip
F1VIZ ?= .venv/bin/f1viz
RUFF ?= .venv/bin/ruff

.PHONY: setup test lint demo clean

setup:
	python3.12 -m venv .venv
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(RUFF) check src tests

demo:
	$(F1VIZ) race analyze --year 2025 --gp monaco --output-dir reports

clean:
	rm -rf .pytest_cache .ruff_cache reports
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

