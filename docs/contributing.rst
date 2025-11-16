Contributing
============

Thank you for considering contributing to rnr! This document provides guidelines for contributing to the project.

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a virtual environment and install development dependencies
4. Install pre-commit hooks
5. Create a new branch for your feature or bugfix

.. code-block:: bash

   git clone https://github.com/yourusername/rnr.git
   cd rnr
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   pre-commit install

Development Workflow
--------------------

1. Create a new branch from ``main``
2. Make your changes
3. Write or update tests
4. Run tests locally
5. Commit your changes (pre-commit hooks will run automatically)
6. Push to your fork
7. Create a pull request

.. code-block:: bash

   git checkout -b feature/my-new-feature
   # Make your changes
   pytest tests/ -v
   git add .
   git commit -m "Add my new feature"
   git push origin feature/my-new-feature

Pre-commit Hooks
----------------

The project uses pre-commit hooks to ensure code quality:

* **Code formatting**: black and isort
* **Linting**: flake8
* **Tests**: pytest runs automatically on commit
* **Coverage**: Coverage check runs on push (requires 80% coverage)

The hooks will run automatically when you commit. If they fail, fix the issues and commit again.

To run hooks manually:

.. code-block:: bash

   pre-commit run --all-files

To skip hooks temporarily (not recommended):

.. code-block:: bash

   git commit --no-verify

Running Tests
-------------

Run all tests:

.. code-block:: bash

   pytest tests/ -v

Run specific test file:

.. code-block:: bash

   pytest tests/test_core.py -v

Run specific test:

.. code-block:: bash

   pytest tests/test_core.py::TestFileDiscovery::test_find_files_recursive -v

Run with coverage:

.. code-block:: bash

   pytest tests/ --cov=rnr --cov-report=html

Code Style
----------

* Follow PEP 8 guidelines
* Use black for code formatting (line length: 100)
* Use isort for import sorting
* Write docstrings for all public functions and classes
* Keep functions focused and single-purpose

Example docstring:

.. code-block:: python

   def find_files(root_path: Path, pattern: str = None, recursive: bool = True) -> List[Path]:
       """
       Find all files in the given path.
       
       Args:
           root_path: Root directory to search
           pattern: Optional pattern to filter filenames
           recursive: Whether to search recursively
           
       Returns:
           List of Path objects for matching files
       """
       # Implementation

Writing Tests
-------------

* Write tests for all new features
* Maintain or improve code coverage
* Use descriptive test names
* Group related tests in test classes
* Use fixtures for common setup

Test structure:

.. code-block:: python

   class TestFeatureName(unittest.TestCase):
       """Test description"""
       
       def setUp(self):
           """Setup test fixtures"""
           pass
       
       def tearDown(self):
           """Cleanup after tests"""
           pass
       
       def test_specific_behavior(self):
           """Test that specific behavior works correctly"""
           # Arrange
           # Act
           # Assert
           pass

Documentation
-------------

* Update documentation for new features
* Include docstrings in code
* Add examples to the examples.rst file
* Update API documentation if needed

Building documentation locally:

.. code-block:: bash

   cd docs
   make html
   # Open _build/html/index.html in browser

Pull Request Guidelines
-----------------------

1. **Title**: Use a clear, descriptive title
2. **Description**: Explain what and why, not just how
3. **Tests**: Include tests for new functionality
4. **Documentation**: Update docs if needed
5. **Commits**: Use meaningful commit messages
6. **CI**: Ensure all CI checks pass

Pull request checklist:

* [ ] Tests pass locally
* [ ] Code coverage maintained or improved
* [ ] Documentation updated
* [ ] Pre-commit hooks pass
* [ ] Commit messages are clear
* [ ] Branch is up to date with main

Reporting Bugs
--------------

When reporting bugs, please include:

* Python version
* Operating system
* rnr version
* Complete error message
* Steps to reproduce
* Expected vs actual behavior

Feature Requests
----------------

Feature requests are welcome! Please:

* Explain the use case
* Describe expected behavior
* Consider backwards compatibility
* Be open to discussion

Code of Conduct
---------------

* Be respectful and inclusive
* Welcome newcomers
* Accept constructive criticism
* Focus on what's best for the project
* Show empathy towards others

Questions?
----------

* Open an issue for bugs or feature requests
* Start a discussion for questions
* Check existing issues and discussions first

Thank You!
----------

Your contributions make this project better. Thank you for taking the time to contribute!