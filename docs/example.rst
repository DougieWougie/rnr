Examples
========

This page contains common use cases and examples for rnr.

Basic Examples
--------------

Replace Spaces with Underscores
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Before: my document.txt, another file.log
   rnr --find " " --replace "_"
   # After: my_document.txt, another_file.log

Change File Extensions
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Before: notes.txt, readme.txt
   rnr --find ".txt" --replace ".md"
   # After: notes.md, readme.md

Remove Patterns
^^^^^^^^^^^^^^^

.. code-block:: bash

   # Before: file_old.txt, document_old.pdf
   rnr --find "_old" --replace ""
   # After: file.txt, document.pdf

Add Prefix to Files
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Before: report.pdf, data.csv
   rnr --find "report" --replace "2024_report"
   rnr --find "data" --replace "2024_data"
   # After: 2024_report.pdf, 2024_data.csv

Intermediate Examples
---------------------

Clean Up Download Filenames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Remove "(1)" from downloaded file copies
   rnr --find " (1)" --replace "" --path ~/Downloads

   # Remove spaces and special characters
   rnr --find " " --replace "_" --path ~/Downloads
   rnr --find "(" --replace "" --path ~/Downloads
   rnr --find ")" --replace "" --path ~/Downloads

Standardize Photo Naming
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Before: IMG_1234.jpg, IMG_1235.jpg
   rnr --find "IMG_" --replace "vacation_" --path ~/Photos/2024
   # After: vacation_1234.jpg, vacation_1235.jpg

Rename Project Files
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Change project prefix across all files
   rnr --find "oldproject" --replace "newproject" --path ~/code/project

Remove Timestamps
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Before: file_2024-01-15.txt
   rnr --find "_2024-01-15" --replace ""
   # After: file.txt

Advanced Examples
-----------------

Process Nested Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Recursively rename all .txt files to .md in a project
   rnr --find ".txt" --replace ".md" --path ~/project --verbose

Non-Recursive Processing
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Only process files in current directory, not subdirectories
   rnr --find " " --replace "_" --no-recursive

Batch Processing with Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a shell script to perform multiple operations:

.. code-block:: bash

   #!/bin/bash
   # cleanup.sh - Clean up file naming conventions

   DIRECTORY="$1"

   echo "Cleaning up files in $DIRECTORY..."

   # Step 1: Replace spaces with underscores
   rnr --find " " --replace "_" --path "$DIRECTORY" --yes

   # Step 2: Remove parentheses
   rnr --find "(" --replace "" --path "$DIRECTORY" --yes
   rnr --find ")" --replace "" --path "$DIRECTORY" --yes

   # Step 3: Lowercase file extensions
   rnr --find ".TXT" --replace ".txt" --path "$DIRECTORY" --yes
   rnr --find ".JPG" --replace ".jpg" --path "$DIRECTORY" --yes

   echo "Cleanup complete!"

Usage:

.. code-block:: bash

   chmod +x cleanup.sh
   ./cleanup.sh ~/Downloads

Real-World Scenarios
--------------------

Organizing Music Collection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Remove unwanted prefixes from song files
   rnr --find "01 - " --replace "" --path ~/Music/Album
   rnr --find "02 - " --replace "" --path ~/Music/Album

   # Standardize format
   rnr --find " - " --replace "_-_" --path ~/Music

Preparing Files for Web Upload
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Make filenames web-safe
   rnr --find " " --replace "-" --path ~/website/assets
   rnr --find "_" --replace "-" --path ~/website/assets

Cleaning Up Screenshots
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Before: Screenshot 2024-01-15 at 10.30.45 AM.png
   rnr --find "Screenshot " --replace "screen_" --path ~/Screenshots
   rnr --find " at " --replace "_" --path ~/Screenshots
   rnr --find ".45 AM" --replace "" --path ~/Screenshots
   rnr --find ".30 PM" --replace "" --path ~/Screenshots

Version Control Cleanup
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Remove backup suffixes
   rnr --find ".bak" --replace "" --path ~/project
   rnr --find "~" --replace "" --path ~/project
   rnr --find ".backup" --replace "" --path ~/project

Renaming After Bulk Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # After extracting an archive with spaces in filenames
   cd extracted_archive/
   rnr --find " " --replace "_" --dry-run  # Preview
   rnr --find " " --replace "_" --yes       # Apply

Tips for Complex Scenarios
---------------------------

Multiple Passes
^^^^^^^^^^^^^^^

For complex renaming, use multiple passes:

.. code-block:: bash

   # Pass 1: Remove unwanted characters
   rnr --find "(" --replace ""
   rnr --find ")" --replace ""

   # Pass 2: Standardize separators
   rnr --find " - " --replace "_"

   # Pass 3: Clean up extensions
   rnr --find ".jpeg" --replace ".jpg"

Testing First
^^^^^^^^^^^^^

Always test on a copy or small subset:

.. code-block:: bash

   # Create test directory
   mkdir test_rename
   cp important_files/*.txt test_rename/

   # Test your rename pattern
   rnr --find " " --replace "_" --path test_rename --dry-run

   # If it looks good, apply to original
   rnr --find " " --replace "_" --path important_files

Pattern Priority
^^^^^^^^^^^^^^^^

Be careful with pattern order when chaining operations:

.. code-block:: bash

   # Wrong: This will create issues
   rnr --find "." --replace "_"  # Replaces ALL dots including extensions!

   # Right: Be more specific
   rnr --find " ." --replace "."  # Only removes spaces before dots