# RNR Testing Guide

This guide explains the testing strategy and how to run tests for rnr.

## Test Structure

RNR has two types of tests:

### Unit Tests (`tests/test_core.py`)
- Test individual functions in isolation
- Fast execution
- Mock external dependencies
- Focus on core logic without CLI

**What they test:**
- File discovery (`find_files`)
- Rename pair generation (`generate_rename_pairs`)
- Conflict detection (`check_conflicts`)
- Rename application (`apply_renames`)
- Edge cases (unicode, special characters, etc.)

### Integration Tests (`tests/test_integration.py`)
- Test full CLI workflows end-to-end
- Slower execution
- Test real subprocess calls
- Verify complete user scenarios

**What they test:**
- Full CLI command execution
- Argument parsing
- User confirmations
- Dry-run mode
- Verbose output
- Error handling
- Conflict detection in real scenarios

## Running Tests

### Quick Commands

```bash
# Run all tests
make test

# Run only unit tests (fast)
make test-unit

# Run only integration tests
make test-integration

# Run with coverage report
make coverage

# Run everything with coverage
make test-all
```

### Using pytest directly

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/test_core.py -v

# Integration tests only
pytest tests/test_integration.py -v

# Specific test class
pytest tests/test_core.py::TestFileDiscovery -v

# Specific test method
pytest tests/test_core.py::TestFileDiscovery::test_find_files_recursive -v

# Tests matching pattern
pytest tests/ -v -k "recursive"

# Stop at first failure
pytest tests/ -v -x

# Run last failed tests
pytest tests/ --lf

# Show print statements
pytest tests/ -v -s
```

### Using test markers

```bash
# Run tests by marker
pytest tests/ -v -m unit
pytest tests/ -v -m integration

# Exclude markers
pytest tests/ -v -m "not integration"

# Multiple markers
pytest tests/ -v -m "unit or integration"
```

## Coverage

### Generate Coverage Report

```bash
# Terminal report
pytest tests/ --cov=rnr --cov-report=term-missing

# HTML report (recommended)
pytest tests/ --cov=rnr --cov-report=html
open htmlcov/index.html

# Both
make coverage
```

### Coverage Requirements

- **Minimum coverage**: 80%
- Enforced in CI/CD
- Enforced in pre-commit hooks (on push)

### Check Coverage

```bash
# Quick check
pytest tests/ --cov=rnr --cov-report=term

# Fail if below threshold
pytest tests/ --cov=rnr --cov-fail-under=80
```

## Pre-commit Testing

Pre-commit hooks automatically run tests:

### On Commit
- Unit tests only (fast feedback)
- Code formatting and linting

### On Push
- All tests with coverage check
- Must pass 80% coverage threshold

### Running Pre-commit Manually

```bash
# Run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run pytest-unit --all-files
pre-commit run pytest-integration --all-files

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

## Writing Tests

### Unit Test Template

```python
import pytest
import unittest
from pathlib import Path

@pytest.mark.unit
class TestNewFeature(unittest.TestCase):
    """Test description"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.test_data = "example"
    
    def tearDown(self):
        """Cleanup after tests"""
        pass
    
    def test_basic_behavior(self):
        """Test that basic behavior works"""
        # Arrange
        input_value = "test"
        
        # Act
        result = function_to_test(input_value)
        
        # Assert
        self.assertEqual(result, expected_value)
```

### Integration Test Template

```python
import pytest
import unittest
import subprocess
import sys

@pytest.mark.integration
class TestCLINewFeature(unittest.TestCase):
    """Integration test for new CLI feature"""
    
    def run_rnr(self, *args, input_text=None):
        """Helper to run rnr CLI"""
        cmd = [sys.executable, "-m", "rnr.cli"] + list(args)
        return subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True
        )
    
    def test_feature_works(self):
        """Test that feature works end-to-end"""
        result = self.run_rnr("--flag", "value")
        self.assertEqual(result.returncode, 0)
```

### Best Practices

1. **Descriptive Names**: Test names should describe what they test
   ```python
   # Good
   def test_find_files_recursive_searches_subdirectories(self):
   
   # Bad
   def test_find_files(self):
   ```

2. **One Assertion Per Test**: Each test should verify one behavior
   ```python
   # Good
   def test_returns_correct_value(self):
       result = function()
       self.assertEqual(result, expected)
   
   def test_raises_error_on_invalid_input(self):
       with self.assertRaises(ValueError):
           function(invalid_input)
   ```

3. **Arrange-Act-Assert**: Structure tests clearly
   ```python
   def test_feature(self):
       # Arrange: Set up test data
       input_data = create_test_data()
       
       # Act: Execute the function
       result = function(input_data)
       
       # Assert: Verify the result
       self.assertEqual(result, expected)
   ```

4. **Cleanup**: Always clean up test files/directories
   ```python
   def setUp(self):
       self.test_dir = tempfile.mkdtemp()
   
   def tearDown(self):
       shutil.rmtree(self.test_dir)
   ```

## Continuous Integration

Tests run automatically on:
- Every push to GitHub
- Every pull request
- Multiple Python versions (3.7-3.11)
- Multiple operating systems (Linux, macOS, Windows)

### CI Configuration

See `.github/workflows/ci.yml` for details:
- Unit tests run first
- Integration tests run next
- Coverage uploaded to Codecov
- Build artifacts created

## Debugging Tests

### Verbose Output

```bash
# Very verbose
pytest tests/ -vv

# Show local variables
pytest tests/ --showlocals

# Full traceback
pytest tests/ --tb=long

# Enter debugger on failure
pytest tests/ --pdb
```

### Print Debugging

```bash
# Show print statements
pytest tests/ -s

# Capture disabled
pytest tests/ --capture=no
```

### Debug Specific Test

```bash
# Run one test with all debug info
pytest tests/test_core.py::TestFileDiscovery::test_find_files_recursive -vv -s --tb=long
```

## Performance Testing

### Time Tests

```bash
# Show slowest tests
pytest tests/ --durations=10

# Show all durations
pytest tests/ --durations=0
```

### Profile Tests

```bash
# Install pytest-profiling
pip install pytest-profiling

# Profile tests
pytest tests/ --profile
```

## Test Coverage Tips

### Find Uncovered Code

```bash
# Generate HTML report
pytest tests/ --cov=rnr --cov-report=html

# Open report
open htmlcov/index.html

# Look for red (uncovered) lines
```

### Test Missing Branches

```bash
# Branch coverage
pytest tests/ --cov=rnr --cov-branch --cov-report=term-missing
```

### Focus on Uncovered Lines

```python
# Use --cov-report to see specific lines
pytest tests/ --cov=rnr --cov-report=term-missing:skip-covered
```

## Common Issues

### Import Errors

```bash
# Install package in editable mode
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

### Tests Failing Locally But Passing in CI

- Check Python version (`python --version`)
- Check dependencies (`pip list`)
- Clean pytest cache (`rm -rf .pytest_cache`)

### Pre-commit Hook Failures

```bash
# Update hooks
pre-commit autoupdate

# Clean and reinstall
pre-commit clean
pre-commit install
```

## Quick Reference

```bash
# Essential Commands
make test                          # Run all tests
make test-unit                     # Unit tests only
make test-integration              # Integration tests only
make coverage                      # Tests + coverage report
pytest tests/ -v -x               # Stop at first failure
pytest tests/ -v -k "pattern"     # Run matching tests
pytest tests/ --lf                # Run last failed
pytest tests/ -m unit             # Run by marker
make clean                        # Clean build artifacts
```

## Need Help?

- Check test output carefully
- Read error messages completely
- Use `-vv` for more details
- Try `--pdb` to debug interactively
- Look at similar tests for examples
- Check GitHub Actions logs for CI failures