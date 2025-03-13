.PHONY: help setup lint test build clean

# Variables
SRC_DIR = validoopsie/
UV_RUN = uv run

# Default target
help:
	@echo "Available targets:"
	@echo "  help     - Show this help message"
	@echo "  setup    - Install dependencies"
	@echo "  lint     - Run linters (flake8, mypy)"
	@echo "  test     - Run tests"
	@echo "  all      - Run lint and test"

setup:
	uv venv --python=python3.9
	uv sync --upgrade --all-groups

lint:
	echo "Running mypy on src/ directory"
	$(UV_RUN) mypy $(SRC_DIR)
	echo "Running ruff check"
	$(UV_RUN) ruff check $(SRC_DIR)
	echo "Running ruff format"
	$(UV_RUN) ruff format $(SRC_DIR)

test:
	echo "Running pytest on src/ directory"
	$(UV_RUN) pytest validoopsie --doctest-modules
	echo "Running pytest on stubs/ directory"
	$(UV_RUN) stubtest validoopsie --allowlist stubtest_allowlist.txt
	echo "Running pytest on examples/ directory"
	$(UV_RUN) python -m doctest validoopsie/validate.pyi
	echo "Running pytest on tests/ directory"
	$(UV_RUN) pytest

all: lint test
