"""
Test Runner for MoneyPrinter V2

Runs all unit tests and generates a comprehensive test report.

Usage:
    python tests/run_all_tests.py

Author: MoneyPrinter V2 Team
License: AGPL-3.0
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def discover_and_run_tests():
    """
    Discover and run all tests in the tests directory.

    Returns:
        bool: True if all tests passed, False otherwise
    """
    print("="*70)
    print("MoneyPrinter V2 - Test Suite")
    print("="*70)
    print()

    # Discover all tests in the tests directory
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print()
    print("="*70)
    print("Test Summary")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = discover_and_run_tests()
    sys.exit(0 if success else 1)
