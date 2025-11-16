.PHONY: help install test test-unit test-integration test-all coverage clean lint format docs

# Variables
PYTHON := python3
PYTEST := pytest
PIP := pip

help:
	@echo "RNR Development Commands"
	@echo "========================"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install package in development mode"
	@echo "  make install-hooks    Install pre-commit hooks"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run all tests"
	@echo "  make test-unit        Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo "  make coverage         Run tests with coverage report"
	@echo "  make test-all         Run all tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Run linters (flake8)"
	@echo "  make format           Format code (black, isort)"
	@echo "  make check            Run all code quality checks"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs             Build documentation"
	@echo "  make docs-serve       Build and serve documentation"
	@echo "  make docs-clean       Clean documentation build"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts"
	@echo "  make clean-all        Remove all generated files"

# Installation
install:
	$(PIP) install -e ".[dev]"

install-hooks:
	pre-commit install

# Testing
test:
	$(PYTEST) tests/ -v

test-unit:
	$(PYTEST) tests/test_core.py -v -m "unit or not integration"

test-integration:
	$(PYTEST) tests/test_integration.py -v -m integration

test-all:
	$(PYTEST) tests/ -v --cov=rnr --cov-report=term-missing --cov-report=html

coverage:
	$(PYTEST) tests/ --cov=rnr --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

# Code quality
lint:
	flake8 rnr/ tests/ --max-line-length=100 --extend-ignore=E203,W503

format:
	black rnr/ tests/ --line-length=100
	isort rnr/ tests/ --profile black --line-length=100

check: lint
	black rnr/ tests/ --check --line-length=100
	isort rnr/ tests/ --check-only --profile black --line-length=100
	@echo "All checks passed!"

# Documentation
docs:
	cd docs && $(MAKE) html

docs-serve: docs
	@echo "Serving documentation at http://localhost:8000"
	cd docs/_build/html && $(PYTHON) -m http.server

docs-clean:
	cd docs && $(MAKE) clean

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

clean-all: clean docs-clean
	rm -rf venv/
	rm -rf .tox/

# Build and distribution
build:
	$(PYTHON) -m build

dist: clean build
	twine check dist/*

# Quick test run for development
quick-test:
	$(PYTEST) tests/test_core.py -v -x

# Run pre-commit hooks on all files
pre-commit:
	pre-commit run --all-files