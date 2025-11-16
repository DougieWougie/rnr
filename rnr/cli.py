#!/usr/bin/env python3
"""
CLI interface for rnr - Recursive file renaming tool
"""

import sys
import argparse
from pathlib import Path
from typing import List, Tuple

from .core import find_files, generate_rename_pairs, check_conflicts, apply_renames
from .colors import Colors


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


def main():
    """Main CLI entry point"""
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