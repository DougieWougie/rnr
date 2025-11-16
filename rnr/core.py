"""
Core functionality for rnr - file discovery and renaming logic
"""

from pathlib import Path
from typing import List, Tuple


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
    """
    Generate old and new path pairs for renaming.
    
    Args:
        files: List of file paths to process
        find: Pattern to find in filenames
        replace: Replacement string
        
    Returns:
        List of tuples (old_path, new_path) for files that will be renamed
    """
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
    """
    Check for naming conflicts in rename operations.
    
    Args:
        rename_pairs: List of (old_path, new_path) tuples
        
    Returns:
        List of conflicting pairs
    """
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


def apply_renames(rename_pairs: List[Tuple[Path, Path]], verbose: bool = False) -> Tuple[int, int]:
    """
    Apply the rename operations.
    
    Args:
        rename_pairs: List of (old_path, new_path) tuples
        verbose: Whether to print detailed output
        
    Returns:
        Tuple of (success_count, error_count)
    """
    from .colors import Colors
    
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