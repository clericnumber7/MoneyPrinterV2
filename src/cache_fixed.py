"""
Cache Management Module for MoneyPrinter V2

This module handles persistent storage of account configurations, posts, videos,
and product information using JSON files in the .mp directory.

All cache operations include proper error handling and data validation to prevent
corruption and data loss.

Author: MoneyPrinter V2 Team
License: AGPL-3.0
"""

import os
import json
from typing import List, Dict, Optional
from config import ROOT_DIR


def get_cache_path() -> str:
    """
    Gets the path to the main cache directory.

    The cache directory stores all persistent data for the application including
    account configurations, generated content metadata, and product information.

    Returns:
        str: Absolute path to the cache directory (.mp folder)

    Example:
        >>> get_cache_path()
        '/path/to/project/.mp'
    """
    return os.path.join(ROOT_DIR, '.mp')


def get_afm_cache_path() -> str:
    """
    Gets the path to the Affiliate Marketing cache file.

    This file stores information about affiliate products and their
    associated social media accounts.

    Returns:
        str: Absolute path to the AFM cache file

    Example:
        >>> get_afm_cache_path()
        '/path/to/project/.mp/afm.json'
    """
    return os.path.join(get_cache_path(), 'afm.json')


def get_twitter_cache_path() -> str:
    """
    Gets the path to the Twitter accounts cache file.

    This file stores Twitter account configurations and post history.

    Returns:
        str: Absolute path to the Twitter cache file

    Example:
        >>> get_twitter_cache_path()
        '/path/to/project/.mp/twitter.json'
    """
    return os.path.join(get_cache_path(), 'twitter.json')


def get_youtube_cache_path() -> str:
    """
    Gets the path to the YouTube accounts cache file.

    This file stores YouTube account configurations and video history.

    Returns:
        str: Absolute path to the YouTube cache file

    Example:
        >>> get_youtube_cache_path()
        '/path/to/project/.mp/youtube.json'
    """
    return os.path.join(get_cache_path(), 'youtube.json')


def _ensure_cache_file_exists(cache_path: str, default_structure: Dict) -> None:
    """
    Ensures a cache file exists with the proper structure.

    If the file doesn't exist, creates it with the default structure.
    This is an internal helper function.

    Args:
        cache_path (str): Path to the cache file
        default_structure (Dict): Default JSON structure to use if file doesn't exist

    Returns:
        None
    """
    if not os.path.exists(cache_path):
        # Ensure the cache directory exists
        cache_dir = os.path.dirname(cache_path)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Create the file with default structure
        with open(cache_path, 'w', encoding='utf-8') as file:
            json.dump(default_structure, file, indent=4)


def _read_cache_file(cache_path: str, default_structure: Dict) -> Dict:
    """
    Safely reads a cache file with error handling.

    Args:
        cache_path (str): Path to the cache file
        default_structure (Dict): Default structure to return on error

    Returns:
        Dict: Parsed JSON data from the cache file
    """
    _ensure_cache_file_exists(cache_path, default_structure)

    try:
        with open(cache_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Validate structure
            if not isinstance(data, dict):
                return default_structure
            return data
    except json.JSONDecodeError:
        # Corrupted JSON, return default
        return default_structure
    except Exception:
        return default_structure


def _write_cache_file(cache_path: str, data: Dict) -> bool:
    """
    Safely writes data to a cache file.

    Args:
        cache_path (str): Path to the cache file
        data (Dict): Data to write

    Returns:
        bool: True if write successful, False otherwise
    """
    try:
        # Write to a temporary file first
        temp_path = cache_path + '.tmp'
        with open(temp_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        # If write successful, replace the original
        if os.path.exists(cache_path):
            os.remove(cache_path)
        os.rename(temp_path, cache_path)

        return True
    except Exception as e:
        print(f"Error writing cache file: {e}")
        # Clean up temp file if it exists
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        return False


def get_accounts(provider: str) -> List[Dict]:
    """
    Gets all accounts for a specific provider from the cache.

    Args:
        provider (str): The provider to get accounts for ("twitter" or "youtube")

    Returns:
        List[Dict]: List of account dictionaries. Returns empty list if none found.

    Raises:
        ValueError: If provider is not "twitter" or "youtube"

    Example:
        >>> accounts = get_accounts("youtube")
        >>> for account in accounts:
        ...     print(account["nickname"])
        'My Channel'
        'Gaming Channel'
    """
    if provider not in ["twitter", "youtube"]:
        raise ValueError(f"Invalid provider: {provider}. Must be 'twitter' or 'youtube'")

    # Determine cache path based on provider
    cache_path = get_twitter_cache_path() if provider == "twitter" else get_youtube_cache_path()

    # Read cache with default structure
    default_structure = {"accounts": []}
    data = _read_cache_file(cache_path, default_structure)

    # Return accounts list
    return data.get('accounts', [])


def add_account(provider: str, account: Dict) -> bool:
    """
    Adds a new account to the cache for the specified provider.

    Args:
        provider (str): The provider ("twitter" or "youtube")
        account (Dict): Account data dictionary containing id, nickname, etc.

    Returns:
        bool: True if account added successfully, False otherwise

    Raises:
        ValueError: If provider is invalid or account data is malformed

    Example:
        >>> account_data = {
        ...     "id": "uuid-here",
        ...     "nickname": "My Account",
        ...     "firefox_profile": "/path/to/profile"
        ... }
        >>> add_account("twitter", account_data)
        True
    """
    if provider not in ["twitter", "youtube"]:
        raise ValueError(f"Invalid provider: {provider}")

    # Validate account has required fields
    if not isinstance(account, dict) or 'id' not in account:
        raise ValueError("Account must be a dictionary with at least an 'id' field")

    # Get cache path
    cache_path = get_twitter_cache_path() if provider == "twitter" else get_youtube_cache_path()

    # Read current accounts
    default_structure = {"accounts": []}
    data = _read_cache_file(cache_path, default_structure)

    # Check if account with this ID already exists
    accounts = data.get('accounts', [])
    existing_ids = [acc.get('id') for acc in accounts]
    if account['id'] in existing_ids:
        print(f"Warning: Account with ID {account['id']} already exists. Skipping.")
        return False

    # Add new account
    accounts.append(account)
    data['accounts'] = accounts

    # Write back to cache
    return _write_cache_file(cache_path, data)


def remove_account(provider: str, account_id: str) -> bool:
    """
    Removes an account from the cache.

    Args:
        provider (str): The provider ("twitter" or "youtube")
        account_id (str): The ID of the account to remove

    Returns:
        bool: True if account removed successfully, False if not found or error

    Example:
        >>> remove_account("twitter", "uuid-123")
        True
    """
    if provider not in ["twitter", "youtube"]:
        raise ValueError(f"Invalid provider: {provider}")

    # Get cache path
    cache_path = get_twitter_cache_path() if provider == "twitter" else get_youtube_cache_path()

    # Read current accounts
    default_structure = {"accounts": []}
    data = _read_cache_file(cache_path, default_structure)

    # Remove the account with matching ID
    accounts = data.get('accounts', [])
    original_count = len(accounts)
    accounts = [account for account in accounts if account.get('id') != account_id]

    # Check if anything was removed
    if len(accounts) == original_count:
        print(f"Warning: No account found with ID {account_id}")
        return False

    data['accounts'] = accounts

    # Write back to cache
    return _write_cache_file(cache_path, data)


def update_account(provider: str, account_id: str, updates: Dict) -> bool:
    """
    Updates an existing account with new data.

    Args:
        provider (str): The provider ("twitter" or "youtube")
        account_id (str): The ID of the account to update
        updates (Dict): Dictionary of fields to update

    Returns:
        bool: True if update successful, False if account not found or error

    Example:
        >>> update_account("youtube", "uuid-123", {"nickname": "New Name"})
        True
    """
    if provider not in ["twitter", "youtube"]:
        raise ValueError(f"Invalid provider: {provider}")

    # Get cache path
    cache_path = get_twitter_cache_path() if provider == "twitter" else get_youtube_cache_path()

    # Read current accounts
    default_structure = {"accounts": []}
    data = _read_cache_file(cache_path, default_structure)

    # Find and update the account
    accounts = data.get('accounts', [])
    account_found = False

    for account in accounts:
        if account.get('id') == account_id:
            account.update(updates)
            account_found = True
            break

    if not account_found:
        print(f"Warning: No account found with ID {account_id}")
        return False

    data['accounts'] = accounts

    # Write back to cache
    return _write_cache_file(cache_path, data)


def get_products() -> List[Dict]:
    """
    Gets all affiliate products from the cache.

    Returns:
        List[Dict]: List of product dictionaries

    Example:
        >>> products = get_products()
        >>> for product in products:
        ...     print(product["affiliate_link"])
    """
    cache_path = get_afm_cache_path()
    default_structure = {"products": []}
    data = _read_cache_file(cache_path, default_structure)
    return data.get("products", [])


def add_product(product: Dict) -> bool:
    """
    Adds a new affiliate product to the cache.

    Args:
        product (Dict): Product data dictionary

    Returns:
        bool: True if product added successfully, False otherwise

    Example:
        >>> product_data = {
        ...     "id": "uuid-here",
        ...     "affiliate_link": "https://amazon.com/...",
        ...     "twitter_uuid": "account-uuid"
        ... }
        >>> add_product(product_data)
        True
    """
    if not isinstance(product, dict) or 'id' not in product:
        raise ValueError("Product must be a dictionary with at least an 'id' field")

    cache_path = get_afm_cache_path()
    default_structure = {"products": []}
    data = _read_cache_file(cache_path, default_structure)

    # Check for duplicate
    products = data.get('products', [])
    existing_ids = [p.get('id') for p in products]
    if product['id'] in existing_ids:
        print(f"Warning: Product with ID {product['id']} already exists. Skipping.")
        return False

    # Add product
    products.append(product)
    data['products'] = products

    return _write_cache_file(cache_path, data)


def get_results_cache_path() -> str:
    """
    Gets the path to the Google Maps scraper results cache file.

    Returns:
        str: Absolute path to the scraper results CSV file

    Example:
        >>> get_results_cache_path()
        '/path/to/project/.mp/scraper_results.csv'
    """
    return os.path.join(get_cache_path(), 'scraper_results.csv')


def clear_cache(provider: Optional[str] = None) -> bool:
    """
    Clears cache files for the specified provider or all caches.

    Args:
        provider (Optional[str]): Specific provider to clear, or None for all

    Returns:
        bool: True if cache cleared successfully

    Example:
        >>> clear_cache("twitter")  # Clear only Twitter cache
        True
        >>> clear_cache()  # Clear all caches
        True
    """
    try:
        if provider == "twitter" or provider is None:
            cache_path = get_twitter_cache_path()
            if os.path.exists(cache_path):
                os.remove(cache_path)

        if provider == "youtube" or provider is None:
            cache_path = get_youtube_cache_path()
            if os.path.exists(cache_path):
                os.remove(cache_path)

        if provider == "afm" or provider is None:
            cache_path = get_afm_cache_path()
            if os.path.exists(cache_path):
                os.remove(cache_path)

        return True
    except Exception as e:
        print(f"Error clearing cache: {e}")
        return False
