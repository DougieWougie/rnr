Installation
============

Requirements
------------

* Python 3.7 or higher
* No external dependencies for core functionality

From PyPI
---------

The easiest way to install rnr is from PyPI using pip:

.. code-block:: bash

   pip install rnr

From Source
-----------

To install from source:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/yourusername/rnr.git
   cd rnr

   # Install
   pip install .

Development Installation
------------------------

For development work, install in editable mode with dev dependencies:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/yourusername/rnr.git
   cd rnr

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install in development mode
   pip install -e ".[dev]"

   # Install pre-commit hooks
   pre-commit install

Verify Installation
-------------------

To verify that rnr is installed correctly:

.. code-block:: bash

   rnr --help

You should see the help message with available options.

Upgrading
---------

To upgrade to the latest version:

.. code-block:: bash

   pip install --upgrade rnr

Uninstallation
--------------

To uninstall rnr:

.. code-block:: bash

   pip uninstall rnr