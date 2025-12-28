"""
Unit Tests for Utility Functions

Tests the fixed utility functions for proper error handling,
cross-platform compatibility, and expected functionality.

Author: MoneyPrinter V2 Team
License: AGPL-3.0
"""

import unittest
import os
import sys
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock ROOT_DIR for testing
import config
test_root = tempfile.mkdtemp()
config.ROOT_DIR = test_root

from utils_fixed import (
    build_url,
    rem_temp_files,
    validate_file_exists,
    ensure_directory_exists
)


class TestBuildUrl(unittest.TestCase):
    """Test YouTube URL building"""

    def test_build_url_valid(self):
        """Test building URL with valid video ID"""
        video_id = "dQw4w9WgXcQ"
        expected = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = build_url(video_id)
        self.assertEqual(result, expected)

    def test_build_url_empty(self):
        """Test building URL with empty video ID"""
        with self.assertRaises(ValueError):
            build_url("")

    def test_build_url_none(self):
        """Test building URL with None"""
        with self.assertRaises(ValueError):
            build_url(None)


class TestRemTempFiles(unittest.TestCase):
    """Test temporary file removal"""

    def setUp(self):
        """Set up test environment"""
        self.mp_dir = os.path.join(test_root, ".mp")
        os.makedirs(self.mp_dir, exist_ok=True)

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.mp_dir):
            shutil.rmtree(self.mp_dir)

    def test_rem_temp_files_empty_dir(self):
        """Test removing files from empty directory"""
        count = rem_temp_files()
        self.assertEqual(count, 0)

    def test_rem_temp_files_with_files(self):
        """Test removing temporary files"""
        # Create test files
        test_files = ["temp1.mp4", "temp2.wav", "cache.json"]
        for filename in test_files:
            with open(os.path.join(self.mp_dir, filename), "w") as f:
                f.write("test")

        # Remove temp files
        count = rem_temp_files()

        # Should remove 2 files (not the JSON)
        self.assertEqual(count, 2)

        # JSON file should still exist
        self.assertTrue(os.path.exists(os.path.join(self.mp_dir, "cache.json")))

        # Other files should be gone
        self.assertFalse(os.path.exists(os.path.join(self.mp_dir, "temp1.mp4")))
        self.assertFalse(os.path.exists(os.path.join(self.mp_dir, "temp2.wav")))

    def test_rem_temp_files_preserves_json(self):
        """Test that JSON files are preserved"""
        # Create JSON files
        json_files = ["cache.json", "config.json", "data.json"]
        for filename in json_files:
            with open(os.path.join(self.mp_dir, filename), "w") as f:
                f.write("{}")

        # Remove temp files
        count = rem_temp_files()
        self.assertEqual(count, 0)

        # All JSON files should still exist
        for filename in json_files:
            self.assertTrue(os.path.exists(os.path.join(self.mp_dir, filename)))

    def test_rem_temp_files_nonexistent_dir(self):
        """Test removing files when directory doesn't exist"""
        # Remove the directory
        shutil.rmtree(self.mp_dir)

        # Should return 0 without crashing
        count = rem_temp_files()
        self.assertEqual(count, 0)


class TestValidateFileExists(unittest.TestCase):
    """Test file validation"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("test content")

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_validate_existing_file(self):
        """Test validating an existing file"""
        result = validate_file_exists(self.test_file, "Test file")
        self.assertTrue(result)

    def test_validate_nonexistent_file(self):
        """Test validating a non-existent file"""
        result = validate_file_exists("/nonexistent/file.txt", "Test file")
        self.assertFalse(result)

    def test_validate_directory_as_file(self):
        """Test validating a directory (should fail)"""
        result = validate_file_exists(self.test_dir, "Test directory")
        self.assertFalse(result)


class TestEnsureDirectoryExists(unittest.TestCase):
    """Test directory creation"""

    def setUp(self):
        """Set up test environment"""
        self.test_root = tempfile.mkdtemp()
        self.test_dir = os.path.join(self.test_root, "test_subdir")

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_root):
            shutil.rmtree(self.test_root)

    def test_ensure_directory_creates_new(self):
        """Test creating a new directory"""
        result = ensure_directory_exists(self.test_dir)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertTrue(os.path.isdir(self.test_dir))

    def test_ensure_directory_existing(self):
        """Test ensuring an existing directory"""
        # Create directory first
        os.makedirs(self.test_dir)

        # Should succeed without error
        result = ensure_directory_exists(self.test_dir)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_dir))

    def test_ensure_nested_directories(self):
        """Test creating nested directories"""
        nested_dir = os.path.join(self.test_root, "level1", "level2", "level3")
        result = ensure_directory_exists(nested_dir)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(nested_dir))


def cleanup():
    """Clean up test environment"""
    if os.path.exists(test_root):
        shutil.rmtree(test_root)


def run_tests():
    """Run all tests"""
    try:
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(sys.modules[__name__])
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return result.wasSuccessful()
    finally:
        cleanup()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
