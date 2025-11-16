# RNR Development Setup Guide

This guide will help you set up the development environment for rnr with all the bells and whistles: pre-commit hooks, tests, and documentation.

## Initial Setup

### 1. Clone and Create Virtual Environment

```bash
git clone https://github.com/yourusername/rnr.git
cd rnr

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Development Dependencies

```bash
# Install package in editable mode with all dev dependencies
pip install -e ".[dev]"
```

This installs:
- pytest and pytest-cov (testing)
- pre-commit (git hooks)
- black and isort (code formatting)
- flake8 (linting)
- sphinx and sphinx-rtd-theme (documentation)

## Pre-commit Hooks Setup

### 3. Install Pre-commit Hooks

```bash
pre-commit install
```

This sets up hooks that run automatically on `git commit`:
- **Code formatting**: black, isort
- **Linting**: flake8
- **Tests**: pytest (runs on commit)
- **Coverage**: pytest with coverage check (runs on push, requires 80%)

### 4. Test Pre-commit Hooks

```bash
# Run hooks manually on all files
pre-commit run --all-files

# Or just make a test commit
git add .
git commit -m "Test commit"
```

The first time you commit, pre-commit will:
1. Format your code with black and isort
2. Lint with flake8
3. Run all tests
4. Only allow commit if everything passes

## Running Tests

### 5. Run Tests Manually

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=rnr --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows

# Run specific test
pytest tests/test_core.py::TestFileDiscovery::test_find_files_recursive -v
```

## Building Documentation

### 6. Build Sphinx Documentation

```bash
cd docs

# Build HTML documentation
make html

# Open in browser
open _build/html/index.html  # macOS
xdg-open _build/html/index.html  # Linux
start _build/html/index.html  # Windows
```

### 7. Check for Broken Links

```bash
cd docs
make linkcheck
```

### 8. Clean Build Files

```bash
cd docs
make clean
```

## Development Workflow

### Typical Development Cycle

```bash
# 1. Create feature branch
git checkout -b feature/my-new-feature

# 2. Make your changes
# Edit files...

# 3. Run tests
pytest tests/ -v

# 4. Commit (pre-commit hooks run automatically)
git add .
git commit -m "Add my new feature"
# Hooks will run: formatting, linting, tests

# 5. If hooks fail, fix issues and commit again
# The hooks will auto-format your code

# 6. Push (coverage check runs)
git push origin feature/my-new-feature
```

### Bypassing Pre-commit Hooks

**Not recommended**, but if needed:

```bash
# Skip hooks for one commit
git commit --no-verify -m "Quick fix"

# Disable hooks temporarily
pre-commit uninstall

# Re-enable hooks
pre-commit install
```

## Code Style Guidelines

The pre-commit hooks enforce these automatically:

- **Line length**: 100 characters (black and flake8)
- **Import sorting**: isort with black profile
- **Docstrings**: All public functions should have docstrings
- **Type hints**: Use type hints where appropriate

## Testing Guidelines

- Write tests for all new features
- Maintain minimum 80% code coverage
- Use descriptive test names
- Group related tests in classes

## Documentation Guidelines

When adding new features:

1. Add docstrings to functions
2. Update relevant .rst files in `docs/`
3. Add examples to `docs/examples.rst`
4. Rebuild docs and verify

## GitHub Actions

Once pushed to GitHub, these workflows run automatically:

- **CI** (`.github/workflows/ci.yml`): Tests on multiple Python versions and OS
- **Docs** (`.github/workflows/docs.yml`): Builds and deploys documentation
- **Release** (`.github/workflows/release.yml`): Publishes to PyPI on tags

## Troubleshooting

### Pre-commit hook fails

```bash
# Update hooks
pre-commit autoupdate

# Run specific hook
pre-commit run black --all-files
```

### Tests fail

```bash
# Run tests with more verbose output
pytest tests/ -vv

# Run tests and stop at first failure
pytest tests/ -x

# Run tests with print statements visible
pytest tests/ -s
```

### Documentation build fails

```bash
# Clean and rebuild
cd docs
make clean
make html
```

### Import errors

```bash
# Reinstall package
pip install -e ".[dev]"
```

## Quick Reference

```bash
# Common Commands
pytest tests/ -v                    # Run tests
pytest tests/ --cov=rnr            # Run tests with coverage
pre-commit run --all-files         # Run all pre-commit hooks
cd docs && make html               # Build documentation
black rnr/ tests/                  # Format code
isort rnr/ tests/                  # Sort imports
flake8 rnr/ tests/                 # Lint code

# Git workflow
git checkout -b feature/name       # Create branch
git add .                          # Stage changes
git commit -m "message"            # Commit (hooks run)
git push origin feature/name       # Push to GitHub
```

## Getting Help

- Check existing GitHub issues
- Read the documentation in `docs/`
- Run `rnr --help` for CLI help
- Look at test examples in `tests/`

Happy coding! 🎉