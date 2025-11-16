Usage
=====

Basic Command Structure
-----------------------

The basic command structure for rnr is:

.. code-block:: bash

   rnr --find PATTERN --replace REPLACEMENT [OPTIONS]

Command-line Options
--------------------

Required Arguments
^^^^^^^^^^^^^^^^^^

``-f, --find FIND``
   Pattern to find in filenames

``-r, --replace REPLACE``
   Replacement string (use empty string "" to remove pattern)

Optional Arguments
^^^^^^^^^^^^^^^^^^

``-p, --path PATH``
   Root path to search (default: current directory)

``--no-recursive``
   Do not search recursively in subdirectories

``-d, --dry-run``
   Preview changes without applying them (highly recommended for first run)

``-y, --yes``
   Skip confirmation prompt and apply changes immediately

``-v, --verbose``
   Show detailed output during renaming operations

``-h, --help``
   Show help message and exit

Common Workflows
----------------

Safe Workflow (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Always start with a dry-run to preview changes:

.. code-block:: bash

   # Step 1: Preview changes
   rnr --find " " --replace "_" --dry-run

   # Step 2: If changes look good, apply them
   rnr --find " " --replace "_"

   # Step 3: Confirm when prompted

Quick Workflow
^^^^^^^^^^^^^^

For experienced users who are confident about the changes:

.. code-block:: bash

   # Apply changes without confirmation
   rnr --find " " --replace "_" --yes

Working with Specific Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Rename files in a specific directory
   rnr --find ".txt" --replace ".md" --path ~/Documents

   # Non-recursive (current directory only)
   rnr --find "old" --replace "new" --no-recursive --path ~/Downloads

Verbose Output
^^^^^^^^^^^^^^

For detailed feedback during renaming:

.. code-block:: bash

   rnr --find " " --replace "_" --verbose

Output Format
-------------

Preview Mode
^^^^^^^^^^^^

When using ``--dry-run``, rnr shows:

* Original filename in red
* New filename in green
* Directory path in blue
* Total number of files to be renamed

Example output::

   Preview of changes:
   ────────────────────────────────────────────────────────────────────────────────

   my file.txt
     → my_file.txt
     /home/user/documents

   another file.log
     → another_file.log
     /home/user/documents

   Total files to rename: 2

Apply Mode
^^^^^^^^^^

When applying changes, rnr shows:

* Confirmation prompt (unless ``--yes`` is used)
* Progress information
* Summary of successful and failed operations

Example output::

   Apply these changes? [y/N] y

   Applying changes...

   Summary:
     ✓ Successfully renamed: 2
     ✗ Failed: 0

Error Handling
--------------

Conflict Detection
^^^^^^^^^^^^^^^^^^

rnr automatically detects conflicts before applying changes:

* Files that already exist with the target name
* Multiple files that would have the same target name

When conflicts are detected, rnr will:

1. Display a warning with conflicting files
2. Refuse to proceed
3. Exit with an error code

Example conflict output::

   Warning: Found 1 naming conflicts:
     ✗ target_file.txt already exists or would be duplicated

   Please resolve conflicts before proceeding.

Permission Errors
^^^^^^^^^^^^^^^^^

If rnr doesn't have permission to rename a file, it will:

* Skip that file
* Continue with other files
* Report the error in the summary

Exit Codes
----------

rnr uses standard exit codes:

* ``0`` - Success (all files renamed successfully or no files to rename)
* ``1`` - Error (conflicts detected, permission errors, or invalid arguments)

Tips and Best Practices
------------------------

1. **Always use dry-run first** - Preview changes before applying them
2. **Be specific with patterns** - More specific patterns reduce unwanted matches
3. **Test on a small directory first** - Verify behavior before running on large directories
4. **Use quotes for patterns with spaces** - ``--find " " --replace "_"``
5. **Keep backups** - For important files, keep backups before bulk renaming
6. **Check for conflicts** - rnr will warn you, but be aware of potential naming conflicts