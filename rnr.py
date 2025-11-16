#!/usr/bin/env python3
"""
rnr - Recursive file renaming tool with pattern matching
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def find_files(root_path: Path, pattern: str = None, recursive: bool = True) -> List[Path]:
    """Find all files in the given path"""
    files = []
    
    if recursive:
        for item in root_path.rglob('*'):
            if item.is_file():
                if pattern is None or pattern in item.name:
                    files.append(item)
    else:
        for item in root_path.glob('*'):
            if item.is_file():
                if pattern is None or pattern in item.name:
                    files.append(item)
    
    return sorted(files)


def generate_rename_pairs(files: List[Path], find: str, replace: str) -> List[Tuple[Path, Path]]:
    """Generate old and new path pairs for renaming"""
    rename_pairs = []
    
    for file_path in files:
        old_name = file_path.name
        new_name = old_name.replace(find, replace)
        
        # Only include if the name actually changes
        if old_name != new_name:
            new_path = file_path.parent / new_name
            rename_pairs.append((file_path, new_path))
    
    return rename_pairs


def check_conflicts(rename_pairs: List[Tuple[Path, Path]]) -> List[Tuple[Path, Path]]:
    """Check for naming conflicts"""
    conflicts = []
    new_paths = set()
    
    for old_path, new_path in rename_pairs:
        # Check if target already exists
        if new_path.exists() and new_path != old_path:
            conflicts.append((old_path, new_path))
        # Check for duplicate target names in this operation
        elif str(new_path) in new_paths:
            conflicts.append((old_path, new_path))
        else:
            new_paths.add(str(new_path))
    
    return conflicts


def preview_changes(rename_pairs: List[Tuple[Path, Path]]):
    """Display preview of changes"""
    if not rename_pairs:
        print(f"{Colors.YELLOW}No files match the pattern.{Colors.RESET}")
        return
    
    print(f"\n{Colors.BOLD}Preview of changes:{Colors.RESET}")
    print(f"{Colors.BLUE}{'─' * 80}{Colors.RESET}\n")
    
    for old_path, new_path in rename_pairs:
        print(f"{Colors.RED}{old_path.name}{Colors.RESET}")
        print(f"  → {Colors.GREEN}{new_path.name}{Colors.RESET}")
        print(f"  {Colors.BLUE}{old_path.parent}{Colors.RESET}\n")
    
    print(f"{Colors.BOLD}Total files to rename: {len(rename_pairs)}{Colors.RESET}")


def apply_renames(rename_pairs: List[Tuple[Path, Path]], verbose: bool = False) -> Tuple[int, int]:
    """Apply the rename operations"""
    success_count = 0
    error_count = 0
    
    for old_path, new_path in rename_pairs:
        try:
            old_path.rename(new_path)
            success_count += 1
            if verbose:
                print(f"{Colors.GREEN}✓{Colors.RESET} {old_path.name} → {new_path.name}")
        except Exception as e:
            error_count += 1
            print(f"{Colors.RED}✗{Colors.RESET} Failed to rename {old_path.name}: {e}")
    
    return success_count, error_count


def main():
    parser = argparse.ArgumentParser(
        description='rnr - Recursively rename files by pattern matching',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview renaming .txt files (dry-run)
  rnr --find ".txt" --replace ".md" --dry-run
  
  # Replace spaces with underscores in current directory
  rnr --find " " --replace "_"
  
  # Rename files in specific directory non-recursively
  rnr --find "old" --replace "new" --path /path/to/dir --no-recursive
  
  # Remove pattern from filenames
  rnr --find "_backup" --replace ""
        """
    )
    
    parser.add_argument(
        '--find', '-f',
        required=True,
        help='Pattern to find in filenames'
    )
    
    parser.add_argument(
        '--replace', '-r',
        required=True,
        help='Replacement string (use empty string "" to remove)'
    )
    
    parser.add_argument(
        '--path', '-p',
        default='.',
        help='Root path to search (default: current directory)'
    )
    
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Do not search recursively'
    )
    
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Preview changes without applying them'
    )
    
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output during renaming'
    )
    
    args = parser.parse_args()
    
    # Validate path
    root_path = Path(args.path).resolve()
    if not root_path.exists():
        print(f"{Colors.RED}Error: Path '{args.path}' does not exist{Colors.RESET}")
        sys.exit(1)
    
    if not root_path.is_dir():
        print(f"{Colors.RED}Error: Path '{args.path}' is not a directory{Colors.RESET}")
        sys.exit(1)
    
    # Find files
    print(f"Searching for files in {Colors.BLUE}{root_path}{Colors.RESET}...")
    recursive = not args.no_recursive
    files = find_files(root_path, args.find, recursive)
    
    # Generate rename pairs
    rename_pairs = generate_rename_pairs(files, args.find, args.replace)
    
    # Preview changes
    preview_changes(rename_pairs)
    
    if not rename_pairs:
        sys.exit(0)
    
    # Check for conflicts
    conflicts = check_conflicts(rename_pairs)
    if conflicts:
        print(f"\n{Colors.RED}{Colors.BOLD}Warning: Found {len(conflicts)} naming conflicts:{Colors.RESET}")
        for old_path, new_path in conflicts[:5]:  # Show first 5
            print(f"  {Colors.RED}✗{Colors.RESET} {new_path.name} already exists or would be duplicated")
        if len(conflicts) > 5:
            print(f"  ... and {len(conflicts) - 5} more")
        print(f"\n{Colors.YELLOW}Please resolve conflicts before proceeding.{Colors.RESET}")
        sys.exit(1)
    
    # Exit if dry-run
    if args.dry_run:
        print(f"\n{Colors.YELLOW}Dry-run mode: No changes were made.{Colors.RESET}")
        sys.exit(0)
    
    # Confirm before applying
    if not args.yes:
        print(f"\n{Colors.YELLOW}Apply these changes? [y/N]{Colors.RESET} ", end='')
        response = input().strip().lower()
        if response not in ('y', 'yes'):
            print("Cancelled.")
            sys.exit(0)
    
    # Apply renames
    print(f"\n{Colors.BOLD}Applying changes...{Colors.RESET}")
    success_count, error_count = apply_renames(rename_pairs, args.verbose)
    
    # Summary
    print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Successfully renamed: {success_count}")
    if error_count > 0:
        print(f"  {Colors.RED}✗{Colors.RESET} Failed: {error_count}")
    
    sys.exit(0 if error_count == 0 else 1)


if __name__ == '__main__':
    main()