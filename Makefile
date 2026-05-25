# Convenience Makefile. Targets:
#   make setup     — build conda env + install pip layer + install pre-commit
#   make verify    — run A.1 acceptance gate
#   make lint      — run pre-commit on all files
#   make test      — run pytest
#   make clean     — remove caches, logs, notebook outputs
#   make help      — list targets

SHELL := /bin/bash
PY := python
CONDA_ENV := thesis-rp

.PHONY: help setup verify lint test clean

help:
	@echo "Targets:"
	@echo "  setup     — mamba env create + pip install + pre-commit install"
	@echo "  verify    — run A.1 acceptance gate (code/utils/verify_a1.py)"
	@echo "  lint      — pre-commit run --all-files"
	@echo "  test      — pytest"
	@echo "  clean     — remove caches, logs, notebook checkpoints"

setup:
	mamba env create -f environment.yml -y || mamba env update -f environment.yml
	@echo ""
	@echo "Activate with:  conda activate $(CONDA_ENV)"
	@echo "Then run:       pip install -r requirements.txt"
	@echo "Then run:       pip install -e ."
	@echo "Then run:       pre-commit install"

verify:
	$(PY) code/utils/verify_a1.py

lint:
	pre-commit run --all-files

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf logs/
	@echo "Caches cleaned."
