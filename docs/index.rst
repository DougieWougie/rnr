Welcome to rnr's documentation!
================================

**rnr** (Recursive File Renamer) is a simple, powerful command-line tool for bulk renaming files using find and replace patterns.

Features
--------

* 🔍 **Recursive or single-directory search** - Search through nested directories or just the current one
* 👀 **Dry-run mode** - Preview changes before applying them
* ⚠️ **Conflict detection** - Prevents overwriting existing files
* 🎨 **Colorized output** - Easy-to-read terminal output
* ✅ **Confirmation prompts** - Safety checks before making changes
* 📝 **Verbose mode** - Detailed feedback during operations

Quick Start
-----------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   pip install rnr

Basic Usage
^^^^^^^^^^^

.. code-block:: bash

   # Preview replacing spaces with underscores (dry-run)
   rnr --find " " --replace "_" --dry-run

   # Replace spaces with underscores
   rnr --find " " --replace "_"

   # Change file extensions
   rnr --find ".txt" --replace ".md"

   # Remove a pattern from filenames
   rnr --find "_backup" --replace ""

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   installation
   usage
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/core
   api/cli
   api/colors

.. toctree::
   :maxdepth: 1
   :caption: Development:

   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`