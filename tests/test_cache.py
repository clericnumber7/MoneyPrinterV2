"""
Unit Tests for Cache Management

Tests cache operations for accounts, products, and data persistence.

Author: MoneyPrinter V2 Team
License: AGPL-3.0
"""

import unittest
import os
import sys
import json
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock ROOT_DIR for testing
import config
test_root = tempfile.mkdtemp()
config.ROOT_DIR = test_root

from cache_fixed import (
    get_cache_path,
    get_accounts,
    add_account,
    remove_account,
    update_account,
    get_products,
    add_product,
    clear_cache
)


class TestCachePaths(unittest.TestCase):
    """Test cache path resolution"""

    def test_get_cache_path(self):
        """Test cache path returns valid directory path"""
        cache_path = get_cache_path()
        self.assertIsInstance(cache_path, str)
        self.assertTrue(cache_path.endswith('.mp'))


class TestAccountManagement(unittest.TestCase):
    """Test account CRUD operations"""

    def setUp(self):
        """Set up test environment before each test"""
        clear_cache()

    def tearDown(self):
        """Clean up after each test"""
        clear_cache()

    def test_get_accounts_empty(self):
        """Test getting accounts when none exist"""
        accounts = get_accounts("twitter")
        self.assertIsInstance(accounts, list)
        self.assertEqual(len(accounts), 0)

    def test_add_account_twitter(self):
        """Test adding a Twitter account"""
        test_account = {
            "id": "test-uuid-123",
            "nickname": "Test Account",
            "firefox_profile": "/path/to/profile",
            "topic": "Technology"
        }

        result = add_account("twitter", test_account)
        self.assertTrue(result)

        # Verify account was added
        accounts = get_accounts("twitter")
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0]["id"], "test-uuid-123")
        self.assertEqual(accounts[0]["nickname"], "Test Account")

    def test_add_account_youtube(self):
        """Test adding a YouTube account"""
        test_account = {
            "id": "test-uuid-456",
            "nickname": "My Channel",
            "firefox_profile": "/path/to/profile",
            "niche": "Gaming",
            "language": "English"
        }

        result = add_account("youtube", test_account)
        self.assertTrue(result)

        # Verify account was added
        accounts = get_accounts("youtube")
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0]["niche"], "Gaming")

    def test_add_duplicate_account(self):
        """Test adding duplicate account (should fail)"""
        test_account = {
            "id": "test-uuid-123",
            "nickname": "Test Account"
        }

        # Add first time
        result1 = add_account("twitter", test_account)
        self.assertTrue(result1)

        # Try to add again (should fail)
        result2 = add_account("twitter", test_account)
        self.assertFalse(result2)

        # Should still only have one account
        accounts = get_accounts("twitter")
        self.assertEqual(len(accounts), 1)

    def test_remove_account(self):
        """Test removing an account"""
        test_account = {
            "id": "test-uuid-789",
            "nickname": "To Remove"
        }

        # Add account
        add_account("twitter", test_account)
        self.assertEqual(len(get_accounts("twitter")), 1)

        # Remove account
        result = remove_account("twitter", "test-uuid-789")
        self.assertTrue(result)

        # Verify removed
        accounts = get_accounts("twitter")
        self.assertEqual(len(accounts), 0)

    def test_remove_nonexistent_account(self):
        """Test removing account that doesn't exist"""
        result = remove_account("twitter", "nonexistent-id")
        self.assertFalse(result)

    def test_update_account(self):
        """Test updating an existing account"""
        test_account = {
            "id": "test-uuid-update",
            "nickname": "Original Name",
            "topic": "Tech"
        }

        # Add account
        add_account("twitter", test_account)

        # Update account
        updates = {
            "nickname": "Updated Name",
            "topic": "Science"
        }
        result = update_account("twitter", "test-uuid-update", updates)
        self.assertTrue(result)

        # Verify updates
        accounts = get_accounts("twitter")
        self.assertEqual(accounts[0]["nickname"], "Updated Name")
        self.assertEqual(accounts[0]["topic"], "Science")

    def test_update_nonexistent_account(self):
        """Test updating account that doesn't exist"""
        result = update_account("twitter", "nonexistent", {"nickname": "Test"})
        self.assertFalse(result)

    def test_invalid_provider(self):
        """Test with invalid provider name"""
        with self.assertRaises(ValueError):
            get_accounts("invalid_provider")

        with self.assertRaises(ValueError):
            add_account("invalid_provider", {"id": "test"})

    def test_account_without_id(self):
        """Test adding account without ID field"""
        invalid_account = {
            "nickname": "No ID"
        }

        with self.assertRaises(ValueError):
            add_account("twitter", invalid_account)


class TestProductManagement(unittest.TestCase):
    """Test affiliate product management"""

    def setUp(self):
        """Set up test environment"""
        clear_cache("afm")

    def tearDown(self):
        """Clean up after tests"""
        clear_cache("afm")

    def test_get_products_empty(self):
        """Test getting products when none exist"""
        products = get_products()
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 0)

    def test_add_product(self):
        """Test adding a product"""
        test_product = {
            "id": "product-123",
            "affiliate_link": "https://amazon.com/product",
            "twitter_uuid": "account-uuid"
        }

        result = add_product(test_product)
        self.assertTrue(result)

        # Verify product was added
        products = get_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["affiliate_link"], "https://amazon.com/product")

    def test_add_duplicate_product(self):
        """Test adding duplicate product"""
        test_product = {
            "id": "product-123",
            "affiliate_link": "https://amazon.com/product"
        }

        # Add first time
        result1 = add_product(test_product)
        self.assertTrue(result1)

        # Try to add again (should fail)
        result2 = add_product(test_product)
        self.assertFalse(result2)

        # Should still only have one product
        products = get_products()
        self.assertEqual(len(products), 1)


class TestCachePersistence(unittest.TestCase):
    """Test that cache persists across operations"""

    def setUp(self):
        """Set up test environment"""
        clear_cache()

    def test_cache_persists(self):
        """Test that cache data persists"""
        # Add account
        test_account = {
            "id": "persist-test",
            "nickname": "Persist Test"
        }
        add_account("twitter", test_account)

        # Get accounts again (simulating new session)
        accounts = get_accounts("twitter")
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0]["id"], "persist-test")

    def test_multiple_accounts_persist(self):
        """Test multiple accounts persist correctly"""
        accounts_to_add = [
            {"id": "acc-1", "nickname": "Account 1"},
            {"id": "acc-2", "nickname": "Account 2"},
            {"id": "acc-3", "nickname": "Account 3"}
        ]

        for acc in accounts_to_add:
            add_account("youtube", acc)

        # Verify all accounts exist
        stored_accounts = get_accounts("youtube")
        self.assertEqual(len(stored_accounts), 3)

        stored_ids = [acc["id"] for acc in stored_accounts]
        self.assertIn("acc-1", stored_ids)
        self.assertIn("acc-2", stored_ids)
        self.assertIn("acc-3", stored_ids)


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
