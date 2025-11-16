#!/usr/bin/env python3
"""
Integration tests for rnr - testing the full CLI workflow
Run with: pytest tests/test_integration.py -v
"""

import unittest
import tempfile
import shutil
import subprocess
import sys
from pathlib import Path
import pytest


@pytest.mark.integration
class TestCLIIntegration(unittest.TestCase):
    """Integration tests for CLI functionality"""
    
    def setUp(self):
        """Create a temporary directory structure for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
        # Create test file structure
        (self.test_path / "file 1.txt").touch()
        (self.test_path / "file 2.txt").touch()
        (self.test_path / "document_old.log").touch()
        
        subdir = self.test_path / "subdir"
        subdir.mkdir()
        (subdir / "nested file.md").touch()
        (subdir / "another_old.txt").touch()
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def run_rnr(self, *args, input_text=None):
        """
        Helper to run rnr CLI command
        
        Args:
            *args: Command line arguments
            input_text: Text to send to stdin (for confirmation prompts)
            
        Returns:
            CompletedProcess with returncode, stdout, stderr
        """
        cmd = [sys.executable, "-m", "rnr.cli"] + list(args)
        result = subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True
        )
        return result
    
    def test_dry_run_mode(self):
        """Test that dry-run mode doesn't modify files"""
        # Run with dry-run
        result = self.run_rnr(
            "--find", " ",
            "--replace", "_",
            "--path", str(self.test_path),
            "--dry-run"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        
        # Files should still have spaces
        self.assertTrue((self.test_path / "file 1.txt").exists())
        self.assertTrue((self.test_path / "file 2.txt").exists())
        self.assertFalse((self.test_path / "file_1.txt").exists())
        
        # Output should mention preview
        self.assertIn("Preview", result.stdout)
        self.assertIn("Dry-run mode", result.stdout)
    
    def test_basic_rename_with_confirmation(self):
        """Test basic rename with yes confirmation"""
        # Run with confirmation 'y'
        result = self.run_rnr(
            "--find", " ",
            "--replace", "_",
            "--path", str(self.test_path),
            "--no-recursive",
            input_text="y\n"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        
        # Files should be renamed
        self.assertFalse((self.test_path / "file 1.txt").exists())
        self.assertFalse((self.test_path / "file 2.txt").exists())
        self.assertTrue((self.test_path / "file_1.txt").exists())
        self.assertTrue((self.test_path / "file_2.txt").exists())
        
        # Output should show success
        self.assertIn("Successfully renamed", result.stdout)
    
    def test_rename_with_yes_flag(self):
        """Test rename with --yes flag (no confirmation)"""
        result = self.run_rnr(
            "--find", "_old",
            "--replace", "_new",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        
        # Files should be renamed
        self.assertFalse((self.test_path / "document_old.log").exists())
        self.assertTrue((self.test_path / "document_new.log").exists())
        
        # Should not ask for confirmation
        self.assertNotIn("Apply these changes?", result.stdout)
    
    def test_recursive_rename(self):
        """Test recursive renaming through subdirectories"""
        result = self.run_rnr(
            "--find", "_old",
            "--replace", "_new",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        
        # Files in root and subdir should be renamed
        self.assertTrue((self.test_path / "document_new.log").exists())
        self.assertTrue((self.test_path / "subdir" / "another_new.txt").exists())
    
    def test_non_recursive_rename(self):
        """Test non-recursive renaming (only current directory)"""
        result = self.run_rnr(
            "--find", " ",
            "--replace", "_",
            "--path", str(self.test_path),
            "--no-recursive",
            "--yes"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        
        # Root files should be renamed
        self.assertTrue((self.test_path / "file_1.txt").exists())
        
        # Subdir files should NOT be renamed
        self.assertTrue((self.test_path / "subdir" / "nested file.md").exists())
        self.assertFalse((self.test_path / "subdir" / "nested_file.md").exists())
    
    def test_no_matches(self):
        """Test behavior when no files match the pattern"""
        result = self.run_rnr(
            "--find", "nonexistent",
            "--replace", "something",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should succeed with no changes
        self.assertEqual(result.returncode, 0)
        
        # Output should indicate no matches
        self.assertIn("No files match", result.stdout)
    
    def test_cancel_confirmation(self):
        """Test canceling operation at confirmation prompt"""
        result = self.run_rnr(
            "--find", " ",
            "--replace", "_",
            "--path", str(self.test_path),
            input_text="n\n"
        )
        
        # Should succeed but not rename
        self.assertEqual(result.returncode, 0)
        
        # Files should not be renamed
        self.assertTrue((self.test_path / "file 1.txt").exists())
        self.assertFalse((self.test_path / "file_1.txt").exists())
        
        # Output should show cancelled
        self.assertIn("Cancelled", result.stdout)
    
    def test_verbose_mode(self):
        """Test verbose output mode"""
        result = self.run_rnr(
            "--find", " ",
            "--replace", "_",
            "--path", str(self.test_path),
            "--verbose",
            "--yes"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        
        # Should show individual file operations
        self.assertIn("✓", result.stdout)
        self.assertIn("→", result.stdout)
    
    def test_invalid_path(self):
        """Test error handling for invalid path"""
        result = self.run_rnr(
            "--find", " ",
            "--replace", "_",
            "--path", "/nonexistent/path/xyz"
        )
        
        # Should fail
        self.assertEqual(result.returncode, 1)
        
        # Should show error message
        self.assertIn("does not exist", result.stderr)
    
    def test_remove_pattern(self):
        """Test removing a pattern from filenames"""
        result = self.run_rnr(
            "--find", "_old",
            "--replace", "",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        
        # Pattern should be removed
        self.assertFalse((self.test_path / "document_old.log").exists())
        self.assertTrue((self.test_path / "document.log").exists())


class TestCLIConflicts(unittest.TestCase):
    """Integration tests for conflict detection"""
    
    def setUp(self):
        """Create test directory with potential conflicts"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def run_rnr(self, *args, input_text=None):
        """Helper to run rnr CLI command"""
        cmd = [sys.executable, "-m", "rnr.cli"] + list(args)
        result = subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True
        )
        return result
    
    def test_existing_file_conflict(self):
        """Test conflict when target file already exists"""
        # Create files that would conflict
        (self.test_path / "file_old.txt").touch()
        (self.test_path / "file_new.txt").touch()  # Target already exists
        
        result = self.run_rnr(
            "--find", "_old",
            "--replace", "_new",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should fail due to conflict
        self.assertEqual(result.returncode, 1)
        
        # Should report conflict
        self.assertIn("conflict", result.stdout.lower())
        self.assertIn("file_new.txt", result.stdout)
        
        # Original file should still exist
        self.assertTrue((self.test_path / "file_old.txt").exists())
    
    def test_duplicate_target_conflict(self):
        """Test conflict when multiple files would have same target name"""
        # Create files that would conflict with each other
        (self.test_path / "file_1_test.txt").touch()
        (self.test_path / "file_2_test.txt").touch()
        
        result = self.run_rnr(
            "--find", "_test",
            "--replace", "",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Both would become "file_1.txt" and "file_2.txt" - no conflict
        # Let's try a real conflict
        (self.test_path / "test_file.txt").touch()
        (self.test_path / "test file.txt").touch()
        
        result = self.run_rnr(
            "--find", " ",
            "--replace", "_",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should detect conflict (both become "test_file.txt")
        self.assertEqual(result.returncode, 1)
        self.assertIn("conflict", result.stdout.lower())


class TestCLIEdgeCases(unittest.TestCase):
    """Integration tests for edge cases"""
    
    def setUp(self):
        """Create test directory"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def run_rnr(self, *args, input_text=None):
        """Helper to run rnr CLI command"""
        cmd = [sys.executable, "-m", "rnr.cli"] + list(args)
        result = subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True
        )
        return result
    
    def test_empty_directory(self):
        """Test behavior with empty directory"""
        result = self.run_rnr(
            "--find", " ",
            "--replace", "_",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should succeed with no changes
        self.assertEqual(result.returncode, 0)
        self.assertIn("No files match", result.stdout)
    
    def test_special_characters(self):
        """Test handling filenames with special characters"""
        (self.test_path / "file (1).txt").touch()
        (self.test_path / "file [copy].txt").touch()
        
        result = self.run_rnr(
            "--find", " (1)",
            "--replace", "",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        self.assertTrue((self.test_path / "file.txt").exists())
    
    def test_unicode_filenames(self):
        """Test handling unicode characters in filenames"""
        (self.test_path / "café_file.txt").touch()
        (self.test_path / "naïve_document.txt").touch()
        
        result = self.run_rnr(
            "--find", "café",
            "--replace", "coffee",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        self.assertTrue((self.test_path / "coffee_file.txt").exists())
    
    def test_hidden_files(self):
        """Test that hidden files are processed"""
        (self.test_path / ".hidden_file").touch()
        (self.test_path / ".config_old").touch()
        
        result = self.run_rnr(
            "--find", "_old",
            "--replace", "_new",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        self.assertTrue((self.test_path / ".config_new").exists())
    
    def test_extension_change(self):
        """Test changing file extensions"""
        (self.test_path / "document.txt").touch()
        (self.test_path / "readme.txt").touch()
        
        result = self.run_rnr(
            "--find", ".txt",
            "--replace", ".md",
            "--path", str(self.test_path),
            "--yes"
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        self.assertTrue((self.test_path / "document.md").exists())
        self.assertTrue((self.test_path / "readme.md").exists())
        self.assertFalse((self.test_path / "document.txt").exists())


class TestCLIArguments(unittest.TestCase):
    """Integration tests for CLI argument handling"""
    
    def run_rnr(self, *args):
        """Helper to run rnr CLI command"""
        cmd = [sys.executable, "-m", "rnr.cli"] + list(args)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        return result
    
    def test_help_flag(self):
        """Test --help flag"""
        result = self.run_rnr("--help")
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        
        # Should show help text
        self.assertIn("usage:", result.stdout.lower())
        self.assertIn("--find", result.stdout)
        self.assertIn("--replace", result.stdout)
    
    def test_missing_required_arguments(self):
        """Test error when required arguments are missing"""
        result = self.run_rnr("--find", "test")
        
        # Should fail
        self.assertEqual(result.returncode, 2)
        
        # Should show error about missing argument
        self.assertIn("required", result.stderr.lower())
    
    def test_short_flags(self):
        """Test short flag versions"""
        test_dir = tempfile.mkdtemp()
        test_path = Path(test_dir)
        (test_path / "test_file.txt").touch()
        
        try:
            result = self.run_rnr(
                "-f", "test",
                "-r", "demo",
                "-p", str(test_path),
                "-y"
            )
            
            # Should succeed
            self.assertEqual(result.returncode, 0)
            self.assertTrue((test_path / "demo_file.txt").exists())
        finally:
            shutil.rmtree(test_dir)


if __name__ == '__main__':
    unittest.main()