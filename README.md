# RNR - Recursive File Renamer

A simple, powerful command-line tool for bulk renaming files using find and replace patterns.

## Features

- 🔍 **Recursive or single-directory search** - Search through nested directories or just the current one
- 👀 **Dry-run mode** - Preview changes before applying them
- ⚠️ **Conflict detection** - Prevents overwriting existing files
- 🎨 **Colorized output** - Easy-to-read terminal output
- ✅ **Confirmation prompts** - Safety checks before making changes
- 📝 **Verbose mode** - Detailed feedback during operations

## Installation

### From source

```bash
# Clone the repository
git clone https://github.com/yourusername/rnr.git
cd rnr

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Requirements

- Python 3.7 or higher
- No external dependencies for core functionality

## Usage

### Basic Examples

```bash
# Preview replacing spaces with underscores (dry-run)
rnr --find " " --replace "_" --dry-run

# Replace spaces with underscores
rnr --find " " --replace "_"

# Change file extensions
rnr --find ".txt" --replace ".md"

# Remove a pattern from filenames
rnr --find "_backup" --replace ""

# Non-recursive (current directory only)
rnr --find "old" --replace "new" --no-recursive

# Work in a specific directory
rnr --find " " --replace "_" --path ~/Documents

# Skip confirmation prompt
rnr --find " " --replace "_" --yes

# Verbose output
rnr --find " " --replace "_" --verbose
```

### Command-line Options

```
usage: rnr [-h] --find FIND --replace REPLACE [--path PATH] [--no-recursive]
           [--dry-run] [--yes] [--verbose]

Options:
  -h, --help            Show help message
  -f, --find FIND       Pattern to find in filenames
  -r, --replace REPLACE Replacement string (use "" to remove)
  -p, --path PATH       Root path to search (default: current directory)
  --no-recursive        Do not search recursively
  -d, --dry-run         Preview changes without applying them
  -y, --yes             Skip confirmation prompt
  -v, --verbose         Show detailed output during renaming
```

## Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run unit tests only (fast)
pytest tests/test_core.py -v

# Run integration tests only
pytest tests/test_integration.py -v

# Run specific test file
pytest tests/test_core.py -v

# Run with coverage report
pytest tests/ --cov=rnr --cov-report=html

# Use Makefile shortcuts
make test              # All tests
make test-unit         # Unit tests only
make test-integration  # Integration tests only
make coverage          # Coverage report
```

For detailed testing documentation, see [TESTING_GUIDE.md](TESTING_GUIDE.md).

### Project Structure

```
rnr/
├── README.md           # This file
├── setup.py           # Package setup configuration
├── rnr/               # Main package
│   ├── __init__.py    # Package initialization
│   ├── core.py        # Core functionality
│   ├── cli.py         # Command-line interface
│   └── colors.py      # Terminal color codes
└── tests/             # Test suite
    ├── __init__.py
    └── test_core.py   # Core functionality tests
```

## Safety Features

RNR includes several safety features to prevent accidental data loss:

1. **Conflict Detection**: Prevents renaming if target files already exist
2. **Dry-run Mode**: Preview all changes before applying them
3. **Confirmation Prompt**: Asks for confirmation before making changes (can be skipped with `-y`)
4. **No Changes to Original**: Files without matching patterns are left untouched

## Examples

### Replace spaces with underscores

```bash
# Before: my document.txt, another file.log
rnr --find " " --replace "_"
# After: my_document.txt, another_file.log
```

### Change file extensions

```bash
# Before: notes.txt, readme.txt
rnr --find ".txt" --replace ".md"
# After: notes.md, readme.md
```

### Remove patterns

```bash
# Before: file_old.txt, document_old.pdf
rnr --find "_old" --replace ""
# After: file.txt, document.pdf
```

### Clean up filenames

```bash
# Before: photo (1).jpg, photo (2).jpg
rnr --find " (" --replace "_("
# After: photo_(1).jpg, photo_(2).jpg
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this tool for any purpose.

## Author

Dougie Richardson

## Acknowledgments

Built with Python 3 and lots of ☕
