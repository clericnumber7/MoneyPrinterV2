"""
Unit Tests for Platform Utilities

Tests cross-platform functionality and dependency checking.

Author: MoneyPrinter V2 Team
License: AGPL-3.0
"""

import unittest
import platform
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from platform_utils import (
    PlatformDetector,
    ProcessManager,
    DependencyChecker,
    PathResolver
)


class TestPlatformDetector(unittest.TestCase):
    """Test cases for PlatformDetector class"""

    def test_os_detection(self):
        """Test that at least one OS is detected"""
        self.assertTrue(
            PlatformDetector.is_windows() or
            PlatformDetector.is_linux() or
            PlatformDetector.is_macos(),
            "Should detect at least one operating system"
        )

    def test_only_one_os_detected(self):
        """Test that only one OS is detected at a time"""
        detected = sum([
            PlatformDetector.is_windows(),
            PlatformDetector.is_linux(),
            PlatformDetector.is_macos()
        ])
        self.assertEqual(detected, 1, "Should detect exactly one operating system")

    def test_get_os_name(self):
        """Test OS name retrieval"""
        os_name = PlatformDetector.get_os_name()
        self.assertIsInstance(os_name, str)
        self.assertTrue(len(os_name) > 0)
        self.assertIn(os_name, ["Windows", "Linux", "macOS"])

    def test_distro_info_on_linux(self):
        """Test Linux distribution info"""
        if PlatformDetector.is_linux():
            info = PlatformDetector.get_distro_info()
            self.assertIsInstance(info, dict)
            # Should have at least NAME field
            self.assertIn("NAME", info)
        else:
            # Should return empty dict on non-Linux
            info = PlatformDetector.get_distro_info()
            self.assertEqual(info, {})


class TestDependencyChecker(unittest.TestCase):
    """Test cases for DependencyChecker class"""

    def test_python_version_check(self):
        """Test Python version validation"""
        is_valid, version_str = DependencyChecker.check_python_version()
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(version_str, str)
        self.assertRegex(version_str, r'\d+\.\d+\.\d+')

        # Since we're running this test, Python must be installed
        version = sys.version_info
        expected_valid = version.major == 3 and version.minor >= 9
        self.assertEqual(is_valid, expected_valid)

    def test_command_exists(self):
        """Test command existence checking"""
        # Python should always exist if we're running tests
        self.assertTrue(DependencyChecker.check_command_exists("python") or
                       DependencyChecker.check_command_exists("python3"))

        # Non-existent command should return False
        self.assertFalse(DependencyChecker.check_command_exists("this_command_does_not_exist_xyz"))

    def test_dependency_report_structure(self):
        """Test dependency report structure"""
        report = DependencyChecker.get_dependency_report()

        self.assertIsInstance(report, dict)
        self.assertIn("python", report)
        self.assertIn("imagemagick", report)
        self.assertIn("firefox", report)
        self.assertIn("go", report)

        # Each dependency should have required fields
        for dep_name, dep_info in report.items():
            self.assertIsInstance(dep_info, dict)
            self.assertIn("installed", dep_info)
            self.assertIn("critical", dep_info)

    def test_imagemagick_check(self):
        """Test ImageMagick detection"""
        is_installed, path = DependencyChecker.check_imagemagick()
        self.assertIsInstance(is_installed, bool)
        if is_installed:
            self.assertIsInstance(path, str)
            self.assertTrue(len(path) > 0)
        else:
            # Path can be None if not installed
            self.assertTrue(path is None or isinstance(path, str))

    def test_firefox_check(self):
        """Test Firefox detection"""
        is_installed, path = DependencyChecker.check_firefox()
        self.assertIsInstance(is_installed, bool)
        if is_installed:
            self.assertIsInstance(path, str)
            self.assertTrue(len(path) > 0)

    def test_go_check(self):
        """Test Go programming language detection"""
        is_installed, version = DependencyChecker.check_go()
        self.assertIsInstance(is_installed, bool)
        if is_installed:
            self.assertIsInstance(version, str)
            self.assertIn("go version", version.lower())


class TestPathResolver(unittest.TestCase):
    """Test cases for PathResolver class"""

    def test_executable_name_windows(self):
        """Test executable name resolution on Windows"""
        if PlatformDetector.is_windows():
            name = PathResolver.get_executable_name("test")
            self.assertEqual(name, "test.exe")
        else:
            name = PathResolver.get_executable_name("test")
            self.assertEqual(name, "test")

    def test_normalize_path(self):
        """Test path normalization"""
        # Test with a relative path
        normalized = PathResolver.normalize_path("./test")
        self.assertTrue(os.path.isabs(normalized))

        # Test with home directory expansion
        if not PlatformDetector.is_windows():
            normalized = PathResolver.normalize_path("~/test")
            self.assertFalse(normalized.startswith("~"))
            self.assertTrue(os.path.isabs(normalized))


class TestProcessManager(unittest.TestCase):
    """Test cases for ProcessManager class"""

    def test_kill_firefox_returns_bool(self):
        """Test that kill_firefox_instances returns boolean"""
        result = ProcessManager.kill_firefox_instances()
        self.assertIsInstance(result, bool)

    def test_kill_process_returns_bool(self):
        """Test that kill_process_by_name returns boolean"""
        result = ProcessManager.kill_process_by_name("nonexistent_process")
        self.assertIsInstance(result, bool)


def run_tests():
    """Run all tests and return results"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
