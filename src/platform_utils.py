"""
Cross-Platform Utility Module for MoneyPrinter V2

This module provides cross-platform compatibility functions that work
consistently across Windows, Linux (Debian/Ubuntu), and macOS.

Author: MoneyPrinter V2 Team
License: AGPL-3.0
"""

import os
import sys
import platform
import subprocess
import shutil
from typing import Optional, Dict, List
from termcolor import colored


class PlatformDetector:
    """
    Detects and provides information about the current operating system platform.

    This class centralizes all platform detection logic to ensure consistent
    behavior across different operating systems (Windows, Linux, macOS).
    """

    @staticmethod
    def is_windows() -> bool:
        """
        Check if the current operating system is Windows.

        Returns:
            bool: True if running on Windows, False otherwise
        """
        return platform.system() == "Windows"

    @staticmethod
    def is_linux() -> bool:
        """
        Check if the current operating system is Linux.

        Returns:
            bool: True if running on Linux, False otherwise
        """
        return platform.system() == "Linux"

    @staticmethod
    def is_macos() -> bool:
        """
        Check if the current operating system is macOS.

        Returns:
            bool: True if running on macOS, False otherwise
        """
        return platform.system() == "Darwin"

    @staticmethod
    def get_os_name() -> str:
        """
        Get a human-readable name of the current operating system.

        Returns:
            str: Name of the operating system (e.g., "Windows", "Linux", "macOS")
        """
        system = platform.system()
        if system == "Darwin":
            return "macOS"
        return system

    @staticmethod
    def get_distro_info() -> Dict[str, str]:
        """
        Get detailed information about the Linux distribution (if applicable).

        Returns:
            Dict[str, str]: Dictionary containing distribution information
                           Returns empty dict if not on Linux
        """
        if not PlatformDetector.is_linux():
            return {}

        try:
            # Try to read /etc/os-release (works on most modern Linux distros)
            if os.path.exists("/etc/os-release"):
                info = {}
                with open("/etc/os-release", "r") as f:
                    for line in f:
                        if "=" in line:
                            key, value = line.strip().split("=", 1)
                            info[key] = value.strip('"')
                return info
        except Exception:
            pass

        return {"NAME": "Unknown Linux"}


class ProcessManager:
    """
    Cross-platform process management utilities.

    Provides consistent methods for starting, stopping, and managing processes
    across different operating systems.
    """

    @staticmethod
    def kill_firefox_instances() -> bool:
        """
        Terminate all running Firefox browser instances.

        This is useful for cleaning up zombie Firefox processes that may
        interfere with Selenium automation.

        Returns:
            bool: True if successfully killed processes, False otherwise
        """
        try:
            if PlatformDetector.is_windows():
                # Windows: Use taskkill
                subprocess.run(
                    ["taskkill", "/F", "/IM", "firefox.exe"],
                    capture_output=True,
                    check=False
                )
            else:
                # Linux/macOS: Use pkill
                subprocess.run(
                    ["pkill", "-9", "firefox"],
                    capture_output=True,
                    check=False
                )
            return True
        except Exception as e:
            print(colored(f"Warning: Could not kill Firefox instances: {e}", "yellow"))
            return False

    @staticmethod
    def kill_process_by_name(process_name: str) -> bool:
        """
        Terminate a process by its name.

        Args:
            process_name (str): Name of the process to terminate

        Returns:
            bool: True if successfully killed process, False otherwise
        """
        try:
            if PlatformDetector.is_windows():
                # Add .exe extension if not present
                if not process_name.endswith(".exe"):
                    process_name += ".exe"
                subprocess.run(
                    ["taskkill", "/F", "/IM", process_name],
                    capture_output=True,
                    check=False
                )
            else:
                # Remove .exe extension if present
                process_name = process_name.replace(".exe", "")
                subprocess.run(
                    ["pkill", "-9", process_name],
                    capture_output=True,
                    check=False
                )
            return True
        except Exception as e:
            print(colored(f"Warning: Could not kill process {process_name}: {e}", "yellow"))
            return False


class DependencyChecker:
    """
    Checks for required system dependencies and provides installation guidance.

    This class verifies that all necessary external tools are installed and
    properly configured before the application runs.
    """

    @staticmethod
    def check_command_exists(command: str) -> bool:
        """
        Check if a command-line tool is available in the system PATH.

        Args:
            command (str): Name of the command to check

        Returns:
            bool: True if command exists, False otherwise
        """
        return shutil.which(command) is not None

    @staticmethod
    def check_python_version() -> tuple[bool, str]:
        """
        Verify that Python version meets the minimum requirement (3.9+).

        Returns:
            tuple[bool, str]: (is_valid, version_string)
        """
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        is_valid = version.major == 3 and version.minor >= 9
        return is_valid, version_str

    @staticmethod
    def check_imagemagick() -> tuple[bool, Optional[str]]:
        """
        Check if ImageMagick is installed and get its path.

        Returns:
            tuple[bool, Optional[str]]: (is_installed, path_to_binary)
        """
        if PlatformDetector.is_windows():
            # On Windows, look for magick.exe
            magick_path = shutil.which("magick")
            return (magick_path is not None, magick_path)
        else:
            # On Linux/macOS, look for convert
            convert_path = shutil.which("convert")
            return (convert_path is not None, convert_path)

    @staticmethod
    def check_firefox() -> tuple[bool, Optional[str]]:
        """
        Check if Firefox is installed.

        Returns:
            tuple[bool, Optional[str]]: (is_installed, path_to_binary)
        """
        if PlatformDetector.is_windows():
            firefox_path = shutil.which("firefox")
            if not firefox_path:
                # Try common installation paths
                common_paths = [
                    r"C:\Program Files\Mozilla Firefox\firefox.exe",
                    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
                ]
                for path in common_paths:
                    if os.path.exists(path):
                        return (True, path)
            return (firefox_path is not None, firefox_path)
        else:
            firefox_path = shutil.which("firefox")
            return (firefox_path is not None, firefox_path)

    @staticmethod
    def check_go() -> tuple[bool, Optional[str]]:
        """
        Check if Go programming language is installed.

        Returns:
            tuple[bool, Optional[str]]: (is_installed, version_string)
        """
        try:
            result = subprocess.run(
                ["go", "version"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                return (True, result.stdout.strip())
            return (False, None)
        except FileNotFoundError:
            return (False, None)

    @staticmethod
    def get_dependency_report() -> Dict[str, Dict[str, any]]:
        """
        Generate a comprehensive report of all system dependencies.

        Returns:
            Dict[str, Dict[str, any]]: Report containing status of all dependencies
        """
        report = {}

        # Python version
        py_valid, py_version = DependencyChecker.check_python_version()
        report["python"] = {
            "installed": True,
            "valid": py_valid,
            "version": py_version,
            "required": "3.9+",
            "critical": True
        }

        # ImageMagick
        im_installed, im_path = DependencyChecker.check_imagemagick()
        report["imagemagick"] = {
            "installed": im_installed,
            "path": im_path,
            "required_for": "Video generation",
            "critical": True
        }

        # Firefox
        ff_installed, ff_path = DependencyChecker.check_firefox()
        report["firefox"] = {
            "installed": ff_installed,
            "path": ff_path,
            "required_for": "Social media automation",
            "critical": True
        }

        # Go
        go_installed, go_version = DependencyChecker.check_go()
        report["go"] = {
            "installed": go_installed,
            "version": go_version,
            "required_for": "Outreach feature only",
            "critical": False
        }

        return report

    @staticmethod
    def print_dependency_report() -> bool:
        """
        Print a formatted dependency report to the console.

        Returns:
            bool: True if all critical dependencies are met, False otherwise
        """
        print(colored("\n" + "="*60, "cyan"))
        print(colored("        SYSTEM DEPENDENCY CHECK", "cyan", attrs=["bold"]))
        print(colored("="*60 + "\n", "cyan"))

        report = DependencyChecker.get_dependency_report()
        all_critical_met = True

        for name, info in report.items():
            status_icon = "✓" if info["installed"] else "✗"
            status_color = "green" if info["installed"] else "red"

            # Check if valid (for Python)
            if "valid" in info:
                if not info["valid"]:
                    status_icon = "✗"
                    status_color = "red"

            is_critical = info.get("critical", False)
            critical_text = " [CRITICAL]" if is_critical else " [OPTIONAL]"

            print(colored(f"{status_icon} {name.upper()}", status_color, attrs=["bold"]), end="")
            print(colored(critical_text, "yellow" if is_critical else "blue"))

            if "version" in info and info["version"]:
                print(f"   Version: {info['version']}")
            if "path" in info and info["path"]:
                print(f"   Path: {info['path']}")
            if "required_for" in info:
                print(f"   Required for: {info['required_for']}")
            if "required" in info:
                print(f"   Minimum required: {info['required']}")

            # Track critical dependencies
            if is_critical and not info["installed"]:
                all_critical_met = False
            if "valid" in info and not info["valid"]:
                all_critical_met = False

            print()  # Blank line between entries

        print(colored("="*60, "cyan"))

        if all_critical_met:
            print(colored("✓ All critical dependencies are satisfied!", "green", attrs=["bold"]))
        else:
            print(colored("✗ Some critical dependencies are missing!", "red", attrs=["bold"]))
            print(colored("\nPlease install missing dependencies before continuing.", "yellow"))

        print(colored("="*60 + "\n", "cyan"))

        return all_critical_met


class PathResolver:
    """
    Resolves file paths in a cross-platform manner.

    Handles differences in path separators and conventions between
    Windows and Unix-like systems.
    """

    @staticmethod
    def get_executable_name(base_name: str) -> str:
        """
        Get the platform-specific executable name.

        Args:
            base_name (str): Base name of the executable (without extension)

        Returns:
            str: Executable name with appropriate extension
        """
        if PlatformDetector.is_windows():
            return f"{base_name}.exe"
        return base_name

    @staticmethod
    def normalize_path(path: str) -> str:
        """
        Normalize a file path for the current platform.

        Args:
            path (str): Path to normalize

        Returns:
            str: Normalized path
        """
        # Convert to absolute path and normalize separators
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        path = os.path.normpath(path)
        return os.path.abspath(path)
