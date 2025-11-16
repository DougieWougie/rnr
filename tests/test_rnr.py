#!/usr/bin/env python3
"""
Unit tests for rnr - Recursive file renaming tool
Run with: python -m pytest test_rnr.py -v
Or: python test_rnr.py
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from typing import List, Tuple

# Import functions from rnr
# Note: In practice, you'd want to structure this as a proper package
# For now, assuming the functions are importable
import sys
sys.path.insert(0, '.')

# Mock the rnr module functions for testing
# In a real setup, you'd import from rnr module


class MockRnr:
    """Mock version of rnr functions for testing"""
    
    @staticmethod
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
    
    @staticmethod
    def generate_rename_pairs(files: List[Path], find: str, replace: str) -> List[Tuple[Path, Path]]:
        """Generate old and new path pairs for renaming"""
        rename_pairs = []
        
        for file_path in files:
            old_name = file_path.name
            new_name = old_name.replace(find, replace)
            
            if old_name != new_name:
                new_path = file_path.parent / new_name
                rename_pairs.append((file_path, new_path))
        
        return rename_pairs
    
    @staticmethod
    def check_conflicts(rename_pairs: List[Tuple[Path, Path]]) -> List[Tuple[Path, Path]]:
        """Check for naming conflicts"""
        conflicts = []
        new_paths = set()
        
        for old_path, new_path in rename_pairs:
            if new_path.exists() and new_path != old_path:
                conflicts.append((old_path, new_path))
            elif str(new_path) in new_paths:
                conflicts.append((old_path, new_path))
            else:
                new_paths.add(str(new_path))
        
        return conflicts


class TestRnrFileDiscovery(unittest.TestCase):
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
        files = MockRnr.find_files(self.test_path, recursive=True)
        self.assertEqual(len(files), 5)
    
    def test_find_files_non_recursive(self):
        """Test non-recursive file discovery"""
        files = MockRnr.find_files(self.test_path, recursive=False)
        self.assertEqual(len(files), 2)
        file_names = [f.name for f in files]
        self.assertIn("file1.txt", file_names)
        self.assertIn("file2.log", file_names)
    
    def test_find_files_with_pattern(self):
        """Test file discovery with pattern matching"""
        files = MockRnr.find_files(self.test_path, pattern=".txt", recursive=True)
        self.assertEqual(len(files), 3)
        for file in files:
            self.assertIn(".txt", file.name)
    
    def test_find_files_no_matches(self):
        """Test file discovery with no matches"""
        files = MockRnr.find_files(self.test_path, pattern=".xyz", recursive=True)
        self.assertEqual(len(files), 0)


class TestRnrRenameLogic(unittest.TestCase):
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
        # Create test files
        file1 = self.test_path / "test_file.txt"
        file2 = self.test_path / "another_test.log"
        file1.touch()
        file2.touch()
        
        files = [file1, file2]
        pairs = MockRnr.generate_rename_pairs(files, "test", "demo")
        
        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs[0][1].name, "demo_file.txt")
        self.assertEqual(pairs[1][1].name, "another_demo.log")
    
    def test_generate_rename_pairs_no_change(self):
        """Test that files without pattern don't get renamed"""
        file1 = self.test_path / "file.txt"
        file1.touch()
        
        files = [file1]
        pairs = MockRnr.generate_rename_pairs(files, "xyz", "abc")
        
        self.assertEqual(len(pairs), 0)
    
    def test_generate_rename_pairs_removal(self):
        """Test removing pattern from filenames"""
        file1 = self.test_path / "file_backup.txt"
        file1.touch()
        
        files = [file1]
        pairs = MockRnr.generate_rename_pairs(files, "_backup", "")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "file.txt")
    
    def test_generate_rename_pairs_multiple_occurrences(self):
        """Test replacing multiple occurrences in filename"""
        file1 = self.test_path / "test_test_file.txt"
        file1.touch()
        
        files = [file1]
        pairs = MockRnr.generate_rename_pairs(files, "test", "demo")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "demo_demo_file.txt")


class TestRnrConflictDetection(unittest.TestCase):
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
        conflicts = MockRnr.check_conflicts(pairs)
        
        self.assertEqual(len(conflicts), 0)
    
    def test_existing_file_conflict(self):
        """Test conflict when target file already exists"""
        file1 = self.test_path / "file1.txt"
        existing = self.test_path / "existing.txt"
        file1.touch()
        existing.touch()
        
        pairs = [(file1, existing)]
        conflicts = MockRnr.check_conflicts(pairs)
        
        self.assertEqual(len(conflicts), 1)
    
    def test_duplicate_target_conflict(self):
        """Test conflict when multiple files would have same target name"""
        file1 = self.test_path / "file1.txt"
        file2 = self.test_path / "file2.txt"
        file1.touch()
        file2.touch()
        
        target = self.test_path / "same_name.txt"
        pairs = [(file1, target), (file2, target)]
        conflicts = MockRnr.check_conflicts(pairs)
        
        self.assertEqual(len(conflicts), 1)


class TestRnrEdgeCases(unittest.TestCase):
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
        files = MockRnr.find_files(self.test_path, recursive=True)
        self.assertEqual(len(files), 0)
    
    def test_special_characters_in_filename(self):
        """Test handling files with special characters"""
        file1 = self.test_path / "file (1).txt"
        file1.touch()
        
        files = [file1]
        pairs = MockRnr.generate_rename_pairs(files, " (1)", "")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "file.txt")
    
    def test_spaces_replacement(self):
        """Test replacing spaces in filenames"""
        file1 = self.test_path / "my test file.txt"
        file1.touch()
        
        files = [file1]
        pairs = MockRnr.generate_rename_pairs(files, " ", "_")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "my_test_file.txt")
    
    def test_extension_replacement(self):
        """Test replacing file extensions"""
        file1 = self.test_path / "document.txt"
        file1.touch()
        
        files = [file1]
        pairs = MockRnr.generate_rename_pairs(files, ".txt", ".md")
        
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1].name, "document.md")


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRnrFileDiscovery))
    suite.addTests(loader.loadTestsFromTestCase(TestRnrRenameLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestRnrConflictDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestRnrEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)