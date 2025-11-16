#!/usr/bin/env python3
"""
Unit tests for rnr core functionality
Run with: pytest tests/test_core.py -v
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import pytest

from rnr.core import (
    find_files,
    generate_rename_pairs,
    check_conflicts,
    apply_renames
)


@pytest.mark.unit
class TestFileDiscovery(unittest.TestCase):
    """Test file discovery functionality"""
    
    def setUp(self):
        """Create a temporary directory structure for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
        # Create test file structure
        # root/
        #   file1.txt
        #   file2.log
        #   subdir1/
        #     file3.txt
        #     file4.md
        #   subdir2/
        #     file5.txt
        
        (self.test_path / "file1.txt").touch()
        (self.test_path / "file2.log").touch()
        
        (self.test_path / "subdir1").mkdir()
        (self.test_path / "subdir1" / "file3.txt").touch()
        (self.test_path / "subdir1" / "file4.md").touch()
        
        (self.test_path / "subdir2").mkdir()
        (self.test_path / "subdir2" / "file5.txt").touch()
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_find_files_recursive(self):
        """Test recursive file discovery"""
        files = find_files(self.test_path, recursive=True)
        self.assertEqual(len(files), 5)
    
    def test_find_files_non_recursive(self):
        """Test non-recursive file discovery"""
        files = find_files(self.test_path, recursive=False)
        self.assertEqual(len(files), 2)
        file_names = [f.name for f in files]
        self.assertIn("file1.txt", file_names)
        self.assertIn("file2.log", file_names)
    
    def test_find_files_with_pattern(self):
        """Test file discovery with pattern matching"""
        files = find_files(self.test_path, pattern=".txt", recursive=True)
        self.assertEqual(len(files), 3)
        for file in files:
            self.assertIn(".txt", file.name)
    
    def test_find_files_no_matches(self):
        """Test file discovery with no matches"""
        files = find_files(self.test_path, pattern=".xyz", recursive=True)
        self.assertEqual(len(files), 0)
    
    def test_find_files_case_sensitive(self):
        """Test that pattern matching is case sensitive"""
        (self.test_path / "FILE_CAPS.TXT").touch()
        files = find_files(self.test_path, pattern=".txt", recursive=False)
        # Should not match .TXT
        self.assertEqual(len(files), 1)


class TestRenameLogic(unittest.TestCase):
    """Test rename pair generation logic"""
    
    def setUp(self):
        """Create temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_generate_rename_pairs_basic(self):
        """Test basic rename pair generation"""
        file1 = self.test_path / "test_file.txt"
        file2 = self.test_path / "another_test.log"
        file1.touch()
        file2.touch()
        
        files = [file1, file2]
        pairs = generate_rename_pairs(files, "test", "demo")
        
        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs[0][1].name, "demo_file.txt")
        self.assertEqual(pairs[1][1].name, "another_demo.log")
    
    def test_generate_rename_pairs_no_change(self):
        """Test that files without pattern don't get renamed"""
        file1 = self.test_path / "file.txt"
        file1.touch()
        
        files = [file1]
        pairs = generate_rename_pairs(files, "xyz", "abc")
        
        self.assertEqual(len(pairs), 0)
    
    def test_generate_rename_pairs_removal(self):
        """Test removing pattern from filenames"""
        file1 = self.test_path / "file_backup.txt"
        file1.touch()
        
        files = [file1]
        pairs = generate_rename_pairs(files, "_backup", "")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "file.txt")
    
    def test_generate_rename_pairs_multiple_occurrences(self):
        """Test replacing multiple occurrences in filename"""
        file1 = self.test_path / "test_test_file.txt"
        file1.touch()
        
        files = [file1]
        pairs = generate_rename_pairs(files, "test", "demo")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "demo_demo_file.txt")
    
    def test_generate_rename_pairs_preserves_path(self):
        """Test that parent directory is preserved"""
        subdir = self.test_path / "subdir"
        subdir.mkdir()
        file1 = subdir / "test_file.txt"
        file1.touch()
        
        files = [file1]
        pairs = generate_rename_pairs(files, "test", "demo")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].parent, subdir)


class TestConflictDetection(unittest.TestCase):
    """Test conflict detection logic"""
    
    def setUp(self):
        """Create temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_no_conflicts(self):
        """Test scenario with no conflicts"""
        file1 = self.test_path / "file1.txt"
        file2 = self.test_path / "file2.txt"
        file1.touch()
        file2.touch()
        
        new1 = self.test_path / "renamed1.txt"
        new2 = self.test_path / "renamed2.txt"
        
        pairs = [(file1, new1), (file2, new2)]
        conflicts = check_conflicts(pairs)
        
        self.assertEqual(len(conflicts), 0)
    
    def test_existing_file_conflict(self):
        """Test conflict when target file already exists"""
        file1 = self.test_path / "file1.txt"
        existing = self.test_path / "existing.txt"
        file1.touch()
        existing.touch()
        
        pairs = [(file1, existing)]
        conflicts = check_conflicts(pairs)
        
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0], (file1, existing))
    
    def test_duplicate_target_conflict(self):
        """Test conflict when multiple files would have same target name"""
        file1 = self.test_path / "file1.txt"
        file2 = self.test_path / "file2.txt"
        file1.touch()
        file2.touch()
        
        target = self.test_path / "same_name.txt"
        pairs = [(file1, target), (file2, target)]
        conflicts = check_conflicts(pairs)
        
        self.assertEqual(len(conflicts), 1)
    
    def test_no_conflict_same_file(self):
        """Test that renaming file to itself is not a conflict"""
        file1 = self.test_path / "file1.txt"
        file1.touch()
        
        pairs = [(file1, file1)]
        conflicts = check_conflicts(pairs)
        
        self.assertEqual(len(conflicts), 0)


class TestApplyRenames(unittest.TestCase):
    """Test actual file renaming operations"""
    
    def setUp(self):
        """Create temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_apply_renames_success(self):
        """Test successful rename operation"""
        file1 = self.test_path / "old_name.txt"
        file1.touch()
        
        new_path = self.test_path / "new_name.txt"
        pairs = [(file1, new_path)]
        
        success, errors = apply_renames(pairs, verbose=False)
        
        self.assertEqual(success, 1)
        self.assertEqual(errors, 0)
        self.assertTrue(new_path.exists())
        self.assertFalse(file1.exists())
    
    def test_apply_renames_multiple(self):
        """Test renaming multiple files"""
        file1 = self.test_path / "file1.txt"
        file2 = self.test_path / "file2.txt"
        file1.touch()
        file2.touch()
        
        new1 = self.test_path / "renamed1.txt"
        new2 = self.test_path / "renamed2.txt"
        pairs = [(file1, new1), (file2, new2)]
        
        success, errors = apply_renames(pairs, verbose=False)
        
        self.assertEqual(success, 2)
        self.assertEqual(errors, 0)
        self.assertTrue(new1.exists())
        self.assertTrue(new2.exists())


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios"""
    
    def setUp(self):
        """Create temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_empty_directory(self):
        """Test behavior with empty directory"""
        files = find_files(self.test_path, recursive=True)
        self.assertEqual(len(files), 0)
    
    def test_special_characters_in_filename(self):
        """Test handling files with special characters"""
        file1 = self.test_path / "file (1).txt"
        file1.touch()
        
        files = [file1]
        pairs = generate_rename_pairs(files, " (1)", "")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "file.txt")
    
    def test_spaces_replacement(self):
        """Test replacing spaces in filenames"""
        file1 = self.test_path / "my test file.txt"
        file1.touch()
        
        files = [file1]
        pairs = generate_rename_pairs(files, " ", "_")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "my_test_file.txt")
    
    def test_extension_replacement(self):
        """Test replacing file extensions"""
        file1 = self.test_path / "document.txt"
        file1.touch()
        
        files = [file1]
        pairs = generate_rename_pairs(files, ".txt", ".md")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "document.md")
    
    def test_unicode_filenames(self):
        """Test handling unicode characters in filenames"""
        file1 = self.test_path / "café_file.txt"
        file1.touch()
        
        files = [file1]
        pairs = generate_rename_pairs(files, "café", "coffee")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "coffee_file.txt")
    
    def test_hidden_files(self):
        """Test that hidden files (starting with .) are found"""
        file1 = self.test_path / ".hidden_file"
        file1.touch()
        
        files = find_files(self.test_path, recursive=False)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, ".hidden_file")


if __name__ == '__main__':
    unittest.main()